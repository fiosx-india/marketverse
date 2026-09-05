"""
=========================================================
MarketVerse AI
Shared Market Context
=========================================================

Purpose
-------
MarketContext is the single shared intelligence context
used by CentralBrain throughout the MarketVerse AI
intelligence pipeline.

Every analysis module contributes evidence to this
context.

MarketContext is a passive data container only.

It NEVER:
- Performs analysis
- Generates predictions
- Calculates risk
- Creates strategies
- Makes final decisions
- Performs orchestration

CentralBrain:
    Controls the workflow.

Guardian:
    Monitors platform health, validation,
    diagnostics, and recovery.

MarketContext:
    Stores shared intelligence evidence.
=========================================================
"""

from datetime import datetime, timezone
import uuid


class MarketContext:
    """
    Shared Market Intelligence Context.

    Responsibilities
    ----------------
    - Store shared market intelligence evidence
    - Store module execution status
    - Store pipeline metadata
    - Track errors
    - Track data freshness

    This class intentionally remains passive.
    """

    # =====================================================
    # ALLOWED CONTEXT SECTIONS
    # =====================================================

    ALLOWED_KEYS = {

        "symbol",

        "market_data",

        "scanner",

        "ai",

        "news",

        "news_analysis",

        "events",

        "technical",

        "pattern",

        "volume",

        "sentiment",

        "prediction",

        "strategy",

        "risk",

        "decision",

        "confidence",

        "probability",

        "opportunity",

        "metadata"
    }

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self, symbol=None):

        created_at = self._timestamp()

        self.data = {

            # =================================================
            # BASIC INFORMATION
            # =================================================

            "symbol": symbol,

            # =================================================
            # RAW MARKET DATA
            # =================================================

            "market_data": None,

            # =================================================
            # MARKET INTELLIGENCE
            # =================================================

            "scanner": {},

            "ai": {},

            # =================================================
            # NEWS INTELLIGENCE
            # =================================================

            "news": {},

            "news_analysis": {},

            "events": {},

            # =================================================
            # MARKET ANALYSIS
            # =================================================

            "technical": {},

            "pattern": {},

            "volume": {},

            "sentiment": {},

            # =================================================
            # PREDICTION
            # =================================================

            "prediction": {},

            # =================================================
            # STRATEGY
            # =================================================

            "strategy": {},

            # =================================================
            # RISK
            # =================================================

            "risk": {},

            # =================================================
            # FINAL DECISION
            # =================================================

            "decision": {},

            # =================================================
            # FUTURE INTELLIGENCE
            # =================================================

            "confidence": {},

            "probability": {},

            "opportunity": {},

            # =================================================
            # PIPELINE METADATA
            # =================================================

            "metadata": {

                "pipeline_id": str(uuid.uuid4()),

                "created_at": created_at,

                "updated_at": created_at,

                "pipeline_status": "created",

                "module_status": {},

                "data_freshness": {},

                "errors": [],

                "update_history": []

            }

        }

    # =====================================================
    # TIMESTAMP
    # =====================================================

    @staticmethod
    def _timestamp():
        """
        Generate UTC timestamp.
        """

        return datetime.now(
            timezone.utc
        ).isoformat()

    # =====================================================
    # COMPLETE CONTEXT
    # =====================================================

    def get(self):
        """
        Return the complete Market Context.
        """

        return self.data

    # =====================================================
    # CONTEXT VALIDATION
    # =====================================================

    def _validate_key(self, key):
        """
        Validate context section name.

        Prevent accidental creation of invalid
        context sections caused by typing mistakes.
        """

        if key not in self.ALLOWED_KEYS:

            raise KeyError(
                f"Invalid MarketContext key: {key}"
            )

    # =====================================================
    # UPDATE CONTEXT SECTION
    # =====================================================

    def update(
        self,
        key,
        value,
        source=None,
        status="success"
    ):
        """
        Update one MarketContext section.

        Parameters
        ----------
        key:
            Context section name.

        value:
            Intelligence evidence or module result.

        source:
            Optional module name.

        status:
            Module execution status.
        """

        self._validate_key(key)

        timestamp = self._timestamp()

        self.data[key] = value

        metadata = self.data["metadata"]

        metadata["updated_at"] = timestamp

        # -------------------------------------------------
        # MODULE STATUS
        # -------------------------------------------------

        metadata["module_status"][key] = {

            "status": status,

            "source": source or key,

            "updated_at": timestamp

        }

        # -------------------------------------------------
        # DATA FRESHNESS
        # -------------------------------------------------

        metadata["data_freshness"][key] = {

            "updated_at": timestamp,

            "source": source or key

        }

        # -------------------------------------------------
        # UPDATE HISTORY
        # -------------------------------------------------

        metadata["update_history"].append({

            "key": key,

            "source": source or key,

            "status": status,

            "timestamp": timestamp

        })

    # =====================================================
    # READ CONTEXT SECTION
    # =====================================================

    def read(
        self,
        key,
        default=None
    ):
        """
        Read one MarketContext section safely.
        """

        return self.data.get(
            key,
            default
        )

    # =====================================================
    # RECORD MODULE FAILURE
    # =====================================================

    def record_error(
        self,
        module,
        error
    ):
        """
        Record module execution failure.

        Recovery is NOT performed here.

        Guardian is responsible for:
        - Diagnostics
        - Validation
        - Recovery
        - Self-healing
        """

        timestamp = self._timestamp()

        metadata = self.data["metadata"]

        metadata["errors"].append({

            "module": module,

            "error": str(error),

            "timestamp": timestamp

        })

        metadata["updated_at"] = timestamp

        # Record failed module status

        metadata["module_status"][module] = {

            "status": "failed",

            "source": module,

            "updated_at": timestamp

        }

    # =====================================================
    # PIPELINE STATUS
    # =====================================================

    def set_pipeline_status(
        self,
        status
    ):
        """
        Update pipeline execution status.

        Examples:

        - created
        - running
        - completed
        - completed_with_errors
        - failed
        """

        metadata = self.data["metadata"]

        metadata["pipeline_status"] = status

        metadata["updated_at"] = self._timestamp()

    # =====================================================
    # PIPELINE STATUS ACCESS
    # =====================================================

    def get_pipeline_status(self):
        """
        Return current pipeline status.
        """

        return self.data[
            "metadata"
        ].get(
            "pipeline_status"
        )

    # =====================================================
    # MODULE STATUS
    # =====================================================

    def get_module_status(
        self,
        key,
        default=None
    ):
        """
        Read execution status for one module.
        """

        return self.data[
            "metadata"
        ][
            "module_status"
        ].get(
            key,
            default
        )

    # =====================================================
    # DATA FRESHNESS
    # =====================================================

    def get_data_freshness(
        self,
        key,
        default=None
    ):
        """
        Return freshness information for
        a specific context section.
        """

        return self.data[
            "metadata"
        ][
            "data_freshness"
        ].get(
            key,
            default
        )

    # =====================================================
    # ERROR ACCESS
    # =====================================================

    def get_errors(self):
        """
        Return all pipeline errors.
        """

        return self.data[
            "metadata"
        ].get(
            "errors",
            []
        )

    # =====================================================
    # ERROR STATUS
    # =====================================================

    def has_errors(self):
        """
        Check whether pipeline contains errors.
        """

        return len(
            self.get_errors()
        ) > 0

    # =====================================================
    # PIPELINE IDENTIFIER
    # =====================================================

    def get_pipeline_id(self):
        """
        Return unique pipeline execution ID.
        """

        return self.data[
            "metadata"
        ].get(
            "pipeline_id"
        )
