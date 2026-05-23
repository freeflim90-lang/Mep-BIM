import argparse
import json

from src.pipeline import run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AI-Powered Energy Consumption Forecasting Pipeline"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="random_forest",
        choices=["random_forest", "linear_regression"],
        help="Model to train.",
    )
    parser.add_argument(
        "--forecast-horizon",
        type=int,
        default=48,
        help="Number of future hours to forecast.",
    )
    parser.add_argument(
        "--test-fraction",
        type=float,
        default=0.2,
        help="Fraction of data reserved for testing.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_pipeline(
        model_name=args.model,
        forecast_horizon=args.forecast_horizon,
        test_fraction=args.test_fraction,
    )

    print("\nPipeline completed successfully.")
    print(f"Model: {result['model_name']}")
    print(f"Forecast horizon: {result['forecast_horizon']} hours")
    print("Metrics:")
    print(json.dumps(result["metrics"], indent=2))
    print("\nSaved artifacts:")
    for key, value in result["artifacts"].items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()

