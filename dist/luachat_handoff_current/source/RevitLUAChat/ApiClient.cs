using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace RevitLUAChat
{
    public class LuaBimChatRequest
    {
        [JsonProperty("user_id")]
        public string UserId { get; set; } = "revit_user";

        [JsonProperty("message")]
        public string Message { get; set; } = string.Empty;

        [JsonProperty("revit_context")]
        public string RevitContext { get; set; } = string.Empty;

        [JsonProperty("client_version")]
        public string ClientVersion { get; set; } = "RevitLUAChat";

        [JsonProperty("source")]
        public string Source { get; set; } = "revit-addin";
    }

    public class LuaBimChatSource
    {
        [JsonProperty("path")]
        public string? Path { get; set; }

        [JsonProperty("score")]
        public int Score { get; set; }
    }

    public class LuaBimChatResponse
    {
        [JsonProperty("status")]
        public string? Status { get; set; }

        [JsonProperty("brand")]
        public string? Brand { get; set; }

        [JsonProperty("agent")]
        public string? Agent { get; set; }

        [JsonProperty("answer")]
        public string? Answer { get; set; }

        [JsonProperty("note_path")]
        public string? NotePath { get; set; }

        [JsonProperty("needs_more")]
        public bool NeedsMore { get; set; }

        [JsonProperty("sources")]
        public List<LuaBimChatSource>? Sources { get; set; }

        [JsonProperty("reason")]
        public string? Reason { get; set; }
    }

    public class LuaBimFeedbackRequest
    {
        [JsonProperty("user_id")]
        public string UserId { get; set; } = "revit_user";

        [JsonProperty("message")]
        public string Message { get; set; } = string.Empty;

        [JsonProperty("answer")]
        public string Answer { get; set; } = string.Empty;

        [JsonProperty("is_good")]
        public bool IsGood { get; set; }

        [JsonProperty("note_path")]
        public string NotePath { get; set; } = string.Empty;

        [JsonProperty("feedback")]
        public string Feedback { get; set; } = string.Empty;
    }

    public class ApiClient
    {
        private static readonly HttpClient client = new HttpClient();
        private const string DefaultBaseUrl = "http://127.0.0.1:8000";
        private const string ClientVersion = "RevitLUAChat-LUA-BIM-LABS-v1";

        private static readonly string BaseUrl =
            (Environment.GetEnvironmentVariable("LUA_BIM_LABS_BACKEND_URL") ?? DefaultBaseUrl).TrimEnd('/');
        private static readonly string ApiKey =
            (Environment.GetEnvironmentVariable("LUA_BIM_LABS_API_KEY") ?? string.Empty).Trim();

        private static string ChatEndpoint => $"{BaseUrl}/api/revit-assistant/chat";
        private static string FeedbackEndpoint => $"{BaseUrl}/api/revit-assistant/feedback";

        public static string LastNotePath { get; private set; } = string.Empty;

        static ApiClient()
        {
            client.Timeout = TimeSpan.FromSeconds(120);
            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
            if (!string.IsNullOrWhiteSpace(ApiKey))
            {
                client.DefaultRequestHeaders.Remove("X-LUA-BIM-API-Key");
                client.DefaultRequestHeaders.Add("X-LUA-BIM-API-Key", ApiKey);
            }
        }

        public static async Task<string> SendMessage(string userId, string message, string revitContext = "")
        {
            try
            {
                var request = new LuaBimChatRequest
                {
                    UserId = userId,
                    Message = message,
                    RevitContext = SanitizeRevitContext(revitContext),
                    ClientVersion = ClientVersion,
                    Source = "revit-addin"
                };

                var json = JsonConvert.SerializeObject(request);
                using (var content = new StringContent(json, Encoding.UTF8, "application/json"))
                using (var response = await client.PostAsync(ChatEndpoint, content))
                {
                    var body = await response.Content.ReadAsStringAsync();
                    if (!response.IsSuccessStatusCode)
                    {
                        return $"LUA BIM LABS backend error ({(int)response.StatusCode}): {body}";
                    }

                    var result = JsonConvert.DeserializeObject<LuaBimChatResponse>(body);
                    if (result == null)
                    {
                        return $"LUA BIM LABS 응답을 해석하지 못했습니다. Raw body: {body}";
                    }

                    if (!string.Equals(result.Status, "ok", StringComparison.OrdinalIgnoreCase))
                    {
                        return $"LUA BIM LABS 요청이 거절되었습니다: {result.Reason ?? body}";
                    }

                    LastNotePath = result.NotePath ?? string.Empty;
                    var answer = result.Answer ?? "LUA BIM LABS가 빈 응답을 반환했습니다.";
                    return Regex.Replace(answer, @"<think>[\s\S]*?</think>", string.Empty, RegexOptions.Singleline).Trim();
                }
            }
            catch (Exception ex)
            {
                return "LUA BIM LABS 백엔드 연결 실패: " + ex.Message + Environment.NewLine +
                       "백엔드 주소는 LUA_BIM_LABS_BACKEND_URL 환경변수로 변경할 수 있습니다.";
            }
        }

        public static async Task SendFeedback(string userId, bool isGood, string userMsg, string botResponse)
        {
            if (string.IsNullOrWhiteSpace(LastNotePath))
            {
                return;
            }

            try
            {
                var request = new LuaBimFeedbackRequest
                {
                    UserId = userId,
                    Message = userMsg,
                    Answer = botResponse,
                    IsGood = isGood,
                    NotePath = LastNotePath,
                    Feedback = isGood ? "Revit Add-in 답변 충분" : "Revit Add-in 답변 보강 필요"
                };

                var json = JsonConvert.SerializeObject(request);
                using (var content = new StringContent(json, Encoding.UTF8, "application/json"))
                {
                    await client.PostAsync(FeedbackEndpoint, content);
                }
            }
            catch
            {
                // 피드백 저장 실패는 채팅 흐름을 막지 않는다.
            }
        }

        private static string SanitizeRevitContext(string context)
        {
            if (string.IsNullOrWhiteSpace(context))
            {
                return string.Empty;
            }

            var sanitized = Regex.Replace(context, @"[A-Za-z]:\\[^\r\n]+", "[LOCAL_PATH_MASKED]");
            sanitized = Regex.Replace(sanitized, @"/Users/[^\r\n]+", "[LOCAL_PATH_MASKED]");
            sanitized = Regex.Replace(sanitized, @"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", "[EMAIL_MASKED]");
            return sanitized.Length > 1500 ? sanitized.Substring(0, 1500) : sanitized;
        }
    }
}
