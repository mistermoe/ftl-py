import os

FTL_SCHEMA_EXTRACTION_MODE_ENV_VAR = "FTL_SCHEMA_EXTRACTION_MODE"

def in_schema_extraction_mode():
    return os.getenv(FTL_SCHEMA_EXTRACTION_MODE_ENV_VAR, "false").lower() == "true"
