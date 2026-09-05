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

MarketContext is a data container only.

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
    Monitors health and validates the system.

MarketContext:
    Stores shared intelligence evidence.
=========================================================
"""

from datetime import datetime, timezone


class MarketContext:
    """
    Shared Market Intelligence Context.

    Stores:

    - Market evidence
    - Analysis results
    - Pipeline metadata
    - Module execution status
    - Data freshness information

    This object remains intentionally passive.
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self, symbol=None):

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

            "ai_market_intelligence": {},

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

                "created_at": self._timestamp(),

                "updated_at": None,

                "pipeline_status": "created",

                "module_status": {},

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
            Execution status.
        """

        self.data[key] = value

        metadata = self.data.get(
            "metadata",
            {}
        )

        timestamp = self._timestamp()

        # -------------------------------------------------
        # Context Update Time
        # -------------------------------------------------

        metadata["updated_at"] = timestamp

        # -------------------------------------------------
        # Module Status
        # -------------------------------------------------

        module_status = metadata.get(
            "module_status",
            {}
        )

        module_status[key] = {

            "status": status,

            "source": source or key,

            "updated_at": timestamp

        }

        metadata["module_status"] = module_status

        # -------------------------------------------------
        # Update History
        # -------------------------------------------------

        history = metadata.get(
            "update_history",
            []
        )

        history.append({

            "key": key,

            "source": source or key,

            "status": status,

            "timestamp": timestamp

        })

        metadata["update_history"] = history

        self.data["metadata"] = metadata

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

        This method does NOT handle recovery.

        Guardian is responsible for:
        - Diagnostics
        - Recovery
        - Validation
        - Self-healing
        """

        metadata = self.data.get(
            "metadata",
            {}
        )

        errors = metadata.get(
            "errors",
            []
        )

        timestamp = self._timestamp()

        errors.append({

            "module": module,

            "error": str(error),

            "timestamp": timestamp

        })

        metadata["errors"] = errors

        self.data["metadata"] = metadata

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
        - failed
        """

        metadata = self.data.get(
            "metadata",
            {}
        )

        metadata[
            "pipeline_status"
        ] = status

        metadata[
            "updated_at"
        ] = self._timestamp()

        self.data[
            "metadata"
        ] = metadata

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

        metadata = self.data.get(
            "metadata",
            {}
        )

        module_status = metadata.get(
            "module_status",
            {}
        )

        return module_status.get(
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

        metadata = self.data.get(
            "metadata",
            {}
        )

        return metadata.get(
            "errors",
            []
        )
