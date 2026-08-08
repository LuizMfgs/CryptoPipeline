import logging

import pandas as pd


logger = logging.getLogger(__name__)


def build_quality_report(
    df: pd.DataFrame,
    quality_result: dict,
) -> dict:

    report = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(
            df.isna().sum().sum()
        ),
        "duplicate_rows": int(
            df.duplicated().sum()
        ),
        "unique_coins": (
            int(df["coin_id"].nunique())
            if "coin_id" in df.columns
            else 0
        ),
        "total_checks": quality_result["total_checks"],
        "passed_checks": quality_result["passed_checks"],
        "failed_checks": quality_result["failed_checks"],
        "status": (
            "PASSED"
            if quality_result["passed"]
            else "FAILED"
        ),
    }

    return report


def log_quality_report(
    report: dict,
    quality_result: dict,
) -> None:

    logger.info(
        "Data Quality Status: %s",
        report["status"],
    )

    logger.info(
        "Rows: %s | Columns: %s",
        report["rows"],
        report["columns"],
    )

    logger.info(
        "Checks: %s/%s passed",
        report["passed_checks"],
        report["total_checks"],
    )

    for result in quality_result["results"]:

        level = (
            logging.INFO
            if result["passed"]
            else logging.ERROR
        )

        logger.log(
            level,
            "[%s] %s - %s",
            "PASS" if result["passed"] else "FAIL",
            result["check"],
            result["message"],
        )


def print_quality_report(
    report: dict,
    quality_result: dict,
) -> None:

    print("\n" + "=" * 60)
    print("DATA QUALITY REPORT")
    print("=" * 60)

    print(f"Rows: {report['rows']}")
    print(f"Columns: {report['columns']}")
    print(f"Missing values: {report['missing_values']}")
    print(f"Duplicate rows: {report['duplicate_rows']}")
    print(f"Unique coins: {report['unique_coins']}")

    print("\nQUALITY CHECKS")
    print("-" * 60)

    for result in quality_result["results"]:

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(
            f"[{status}] "
            f"{result['check']}: "
            f"{result['message']}"
        )

    print("\n" + "=" * 60)

    print(
        f"STATUS: {report['status']} "
        f"({report['passed_checks']}/"
        f"{report['total_checks']} checks passed)"
    )

    print("=" * 60)