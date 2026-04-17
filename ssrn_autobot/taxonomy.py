"""Research taxonomy, keywords, and label mappings."""

from __future__ import annotations

TOPIC_KEYWORDS: dict[str, tuple[list[str], int]] = {
    "sdf_factor_pricing": (
        [
            "stochastic discount factor",
            "pricing kernel",
            "hansen-jagannathan",
            "factor pricing",
            "no-arbitrage",
            "identification",
            "sdf",
        ],
        12,
    ),
    "anomalies_expected_returns": (
        ["anomalies", "expected returns", "return predictability", "mispricing", "risk-based"],
        8,
    ),
    "unpriced_weak_factors": (
        ["unpriced factor", "weak factor", "factor misspecification", "factor selection"],
        11,
    ),
    "icc_valuation_accounting": (
        ["implied cost of capital", "icc", "valuation", "profitability", "investment"],
        9,
    ),
    "ivol_derivatives": (
        ["idiosyncratic volatility", "pure ivol", "variance risk premium", "option-implied", "derivatives"],
        9,
    ),
    "term_structure_equity": (
        ["term structure of equity", "dividend strips", "equity duration", "horizon-specific"],
        11,
    ),
    "gmv_zero_beta": (
        ["gmv", "global minimum variance", "zero-beta", "robust portfolio"],
        10,
    ),
    "covariance_shrinkage": (
        ["covariance shrinkage", "high-dimensional covariance", "random matrix", "poet"],
        11,
    ),
    "asset_allocation": (
        ["asset allocation", "dynamic allocation", "life-cycle investing"],
        10,
    ),
    "target_date_fund": (
        ["target date fund", "glide path", "retirement portfolio"],
        10,
    ),
}

IRRELEVANT_KEYWORDS: list[str] = [
    "clinical trial",
    "biology",
    "cryptography protocol",
    "geology",
    "neuroscience",
    "pure marketing",
]

PROJECT_LABEL_RULES: dict[str, list[str]] = {
    "project_sdf_estimation": ["stochastic discount factor", "pricing kernel", "hansen-jagannathan", "sdf"],
    "project_unpriced_factor": ["unpriced factor", "weak factor", "factor misspecification", "factor selection"],
    "project_pure_ivol": ["idiosyncratic volatility", "pure ivol", "variance risk premium", "option-implied"],
    "project_icc_profitability_investment": ["implied cost of capital", "icc", "profitability", "investment"],
    "project_term_structure_equity": ["term structure of equity", "dividend strips", "equity duration"],
    "project_gmv_zero_beta": ["gmv", "zero-beta", "robust portfolio"],
    "project_covariance_shrinkage": ["covariance shrinkage", "random matrix", "poet", "high-dimensional covariance"],
    "project_asset_allocation": ["asset allocation", "dynamic allocation", "life-cycle investing"],
    "project_target_date_fund": ["target date fund", "glide path", "retirement portfolio"],
    "project_finance_accounting_bridge": ["accounting", "valuation", "implied cost of capital"],
}
