import os
from typing import Any

import httpx

from backend.model_routing import model_routing_status
from backend.text_utils import append_korean_response_instruction, contains_likely_chinese_text


DEFAULT_PROVIDER = "ollama"
DEFAULT_CODER_MODEL = "qwen2.5-coder:7b"
DEFAULT_QA_MODEL = "qwen2.5:7b"
DEFAULT_BASE_URL = "http://127.0.0.1:11434"


def enabled() -> bool:
    return os.environ.get("LOCAL_CODER_ENABLED", "false").lower() in {"1", "true", "yes", "on"}


def provider() -> str:
    return os.environ.get("LOCAL_CODER_PROVIDER", DEFAULT_PROVIDER)


def model() -> str:
    """코드 생성 전용 모델 (LOCAL_CODER_MODEL)."""
    return os.environ.get("LOCAL_CODER_MODEL", DEFAULT_CODER_MODEL)


def qa_model() -> str:
    """자연어 Q&A 합성 전용 모델 (KNOWLEDGE_QA_MODEL). 미설정 시 코더 모델로 폴백."""
    return os.environ.get("KNOWLEDGE_QA_MODEL", model())


def base_url() -> str:
    return os.environ.get("LOCAL_CODER_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


async def _check_model_available(target_model: str) -> dict[str, Any]:
    """지정한 모델이 Ollama에 있는지 확인한다."""
    url = base_url()
    try:
        async with httpx.AsyncClient(timeout=4) as client:
            tags_response = await client.get(f"{url}/api/tags")
    except httpx.HTTPError as exc:
        return {"reachable": False, "reason": str(exc), "available_models": [], "model_available": False}

    if tags_response.status_code >= 400:
        return {
            "reachable": False,
            "reason": f"ollama status {tags_response.status_code}",
            "available_models": [],
            "model_available": False,
        }

    available = [item.get("name") for item in tags_response.json().get("models", []) if item.get("name")]
    base = target_model.split(":")[0] + ":"
    return {
        "reachable": True,
        "available_models": available,
        "model_available": target_model in available or any(name.startswith(base) for name in available),
    }


async def check_ollama_status() -> dict[str, Any]:
    """코더 모델 기준 Ollama 상태 확인 (하위 호환)."""
    return await _check_model_available(model())


async def status() -> dict[str, Any]:
    """코더 모델 상태 (하위 호환용)."""
    current_provider = provider()
    result = {
        "enabled": enabled(),
        "provider": current_provider,
        "model": model(),
        "qa_model": qa_model(),
        "base_url": base_url(),
        "recommended_role": "local_first_pass_developer",
        "routing": model_routing_status().get("local", {}),
        "rules": [
            "Autodesk API 의존이 없는 일반 개발은 로컬 1차 구현 초안 작성에 사용",
            "Revit/Navisworks API 의존 작업은 초안/정적 검토까지만 수행",
            "모델 변경, 빌드, Store 제출 확정은 최고지배자 실기 테스트 후 진행",
        ],
    }
    if current_provider == "ollama":
        result.update(await check_ollama_status())
    else:
        result.update({
            "reachable": False,
            "reason": "현재는 ollama provider 상태 확인만 지원합니다.",
            "available_models": [],
            "model_available": False,
        })
    return result


async def _generate_with_model(
    target_model: str,
    prompt: str,
    system: str = "",
    temperature: float = 0.2,
    num_predict: int = 360,
    timeout: int = 45,
) -> dict[str, Any]:
    """지정 모델로 Ollama generate 호출."""
    if not enabled():
        return {"ok": False, "reason": "LOCAL_CODER_ENABLED=false", "response": ""}

    ollama_status = await _check_model_available(target_model)
    if not ollama_status.get("reachable"):
        return {"ok": False, "reason": ollama_status.get("reason", "ollama not reachable"), "response": ""}
    if not ollama_status.get("model_available"):
        return {"ok": False, "reason": f"model not available: {target_model}", "response": ""}

    payload = {
        "model": target_model,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_ctx": 8192,
            "num_predict": max(64, min(num_predict, 1200)),
        },
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(f"{base_url()}/api/generate", json=payload)
    if response.status_code >= 400:
        return {"ok": False, "reason": f"ollama generate status {response.status_code}: {response.text}", "response": ""}
    data = response.json()
    return {
        "ok": True,
        "reason": "",
        "response": data.get("response", "").strip(),
        "model": data.get("model", target_model),
    }


async def generate(
    prompt: str,
    system: str = "",
    temperature: float = 0.2,
    num_predict: int = 360,
    timeout: int = 45,
) -> dict[str, Any]:
    """코드 생성 전용 — LOCAL_CODER_MODEL 사용."""
    return await _generate_with_model(
        target_model=model(),
        prompt=prompt,
        system=system,
        temperature=temperature,
        num_predict=num_predict,
        timeout=timeout,
    )


async def generate_qa(
    prompt: str,
    system: str = "",
    temperature: float = 0.3,
    num_predict: int = 600,
    timeout: int = 45,
) -> dict[str, Any]:
    """자연어 Q&A 합성 전용 — KNOWLEDGE_QA_MODEL 사용. 미설정 시 코더 모델 폴백."""
    target = qa_model()
    qa_system = append_korean_response_instruction(system)
    qa_prompt = (
        f"{prompt}\n\n"
        "중요: 최종 답변은 반드시 한국어로만 작성하세요. 중국어 문장이나 중국어식 표현을 섞지 마세요."
    )
    result = await _generate_with_model(
        target_model=target,
        prompt=qa_prompt,
        system=qa_system,
        temperature=temperature,
        num_predict=num_predict,
        timeout=timeout,
    )
    # QA 모델 실패 시 코더 모델로 재시도
    if not result.get("ok") and target != model():
        result = await _generate_with_model(
            target_model=model(),
            prompt=qa_prompt,
            system=qa_system,
            temperature=temperature,
            num_predict=num_predict,
            timeout=timeout,
        )
    if result.get("ok") and contains_likely_chinese_text(result.get("response", "")):
        retry_prompt = (
            f"{qa_prompt}\n\n"
            "방금 응답에 중국어 문장이 섞였습니다. 같은 내용을 한국어 존댓말로 다시 작성하세요. "
            "중국어 한자 문장을 포함하지 마세요."
        )
        result = await _generate_with_model(
            target_model=target,
            prompt=retry_prompt,
            system=qa_system,
            temperature=temperature,
            num_predict=num_predict,
            timeout=timeout,
        )
    return result
