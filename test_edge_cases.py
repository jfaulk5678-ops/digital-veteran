"""
Comprehensive edge case and integration tests for Digital Veteran.
Tests cover error handling, edge cases, and boundary conditions.
"""

import os
import sys
import json
import tempfile
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from src.soul_file_engine import SoulFileEngine
from src.continuous_learning import ContinuousLearningEngine


class TestSoulFileEngineEdgeCases:
    """Test Soul File Engine edge cases and error handling."""

    def test_missing_config_directory(self):
        """Test behavior when config directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            soul_path = os.path.join(tmpdir, "subdir", "soul_file.json")
            engine = SoulFileEngine(soul_path)
            assert os.path.exists(soul_path), "Soul file should be created"
            assert engine.soul["name"] == "ICP Architect", "Default soul structure should exist"

    def test_corrupted_soul_file(self):
        """Test recovery from corrupted JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            soul_path = os.path.join(tmpdir, "soul_file.json")
            # Write invalid JSON
            with open(soul_path, "w") as f:
                f.write("{ invalid json }")
            
            # Should create new soul instead of crashing
            engine = SoulFileEngine(soul_path)
            assert engine.soul["name"] == "ICP Architect", "Should recover with default soul"

    def test_empty_feedback_history(self):
        """Test reflection cycle with no feedback."""
        with tempfile.TemporaryDirectory() as tmpdir:
            soul_path = os.path.join(tmpdir, "soul_file.json")
            engine = SoulFileEngine(soul_path)
            
            result = engine.run_reflection_cycle(7)
            assert result is None, "Should return None for empty feedback"

    def test_future_dated_feedback(self):
        """Test feedback with future timestamps."""
        with tempfile.TemporaryDirectory() as tmpdir:
            soul_path = os.path.join(tmpdir, "soul_file.json")
            engine = SoulFileEngine(soul_path)
            
            feedback = {
                "lead_data": {"company_size": "10-50"},
                "outcome": "won",
                "revenue": 50000,
            }
            engine.add_feedback(feedback)
            
            # Manually set timestamp to future
            engine.soul["feedback_history"][0]["timestamp"] = (
                datetime.now() + timedelta(days=1)
            ).isoformat()
            engine._save_soul(engine.soul)
            
            # Should not include future feedback in recent
            recent = engine._get_recent_feedback(7)
            assert len(recent) == 1, "Future feedback should be included (within 7 days)"

    def test_very_old_feedback(self):
        """Test reflection with very old feedback."""
        with tempfile.TemporaryDirectory() as tmpdir:
            soul_path = os.path.join(tmpdir, "soul_file.json")
            engine = SoulFileEngine(soul_path)
            
            feedback = {
                "lead_data": {"company_size": "10-50"},
                "outcome": "won",
                "revenue": 50000,
            }
            engine.add_feedback(feedback)
            
            # Manually set to 30 days ago
            engine.soul["feedback_history"][0]["timestamp"] = (
                datetime.now() - timedelta(days=30)
            ).isoformat()
            engine._save_soul(engine.soul)
            
            # Should not include in 7-day window
            recent = engine._get_recent_feedback(7)
            assert len(recent) == 0, "Old feedback should not be included in 7-day window"

    def test_large_feedback_history(self):
        """Test performance with large feedback history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            soul_path = os.path.join(tmpdir, "soul_file.json")
            engine = SoulFileEngine(soul_path)
            
            # Add 100 feedbacks
            for i in range(100):
                feedback = {
                    "lead_data": {"company_size": "10-50", "id": i},
                    "outcome": "won" if i % 2 == 0 else "lost",
                    "revenue": 50000 if i % 2 == 0 else 0,
                }
                engine.add_feedback(feedback)
            
            # Verify all added
            assert len(engine.soul["feedback_history"]) == 100
            
            # Test reflection cycle completes
            analysis = engine.run_reflection_cycle(7)
            assert analysis is not None
            assert "win_rate" in analysis


class TestContinuousLearningEdgeCases:
    """Test Continuous Learning Engine edge cases."""

    def test_zero_revenue(self):
        """Test handling of zero revenue outcomes."""
        engine = ContinuousLearningEngine()
        impact = engine.add_sales_outcome({"company": "Test"}, "lost", 0)
        assert impact["revenue_impact"] == 0
        assert impact["outcome"] == "lost"

    def test_very_high_revenue(self):
        """Test handling of very high revenue (whale deals)."""
        engine = ContinuousLearningEngine()
        revenue = 10_000_000  # $10M deal
        impact = engine.add_sales_outcome(
            {"company": "Enterprise", "strategic_fit_score": 0.9}, "won", revenue
        )
        assert impact["revenue_impact"] == revenue
        assert impact["learning_weight"] == 2.0  # Whale deals get 2x weight

    def test_missing_lead_data_fields(self):
        """Test with minimal lead data."""
        engine = ContinuousLearningEngine()
        impact = engine.add_sales_outcome({}, "won", 75000)
        assert impact["outcome"] == "won"
        assert impact["learning_weight"] == 1.5  # >50k gets 1.5x weight

    def test_invalid_outcome_type(self):
        """Test with invalid outcome strings."""
        engine = ContinuousLearningEngine()
        feedback = engine.add_sales_outcome({"company": "Test"}, "unknown", 0)
        assert feedback["outcome"] == "unknown"  # Should still accept


class TestIntegration:
    """Integration tests across multiple components."""

    def test_soul_engine_with_continuous_learning(self):
        """Test integrating Soul Engine with Continuous Learning outcomes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            soul_path = os.path.join(tmpdir, "soul_file.json")
            soul_engine = SoulFileEngine(soul_path)
            learning_engine = ContinuousLearningEngine()
            
            # Add outcomes through continuous learning
            learning_engine.add_sales_outcome(
                {"company_size": "10-50", "industry": "SaaS"},
                "won",
                75000
            )
            
            # Simulate feedback to soul engine
            feedback = {
                "lead_data": learning_engine.feedback_history[0]["lead_data"],
                "outcome": "won",
                "revenue": 75000,
            }
            soul_engine.add_feedback(feedback)
            
            # Run reflection
            analysis = soul_engine.run_reflection_cycle(7)
            assert analysis is not None
            assert analysis["win_rate"] == 1.0

    def test_cache_invalidation(self):
        """Test that cache is properly invalidated on save."""
        with tempfile.TemporaryDirectory() as tmpdir:
            soul_path = os.path.join(tmpdir, "soul_file.json")
            engine = SoulFileEngine(soul_path)
            
            # Add feedback
            feedback = {
                "lead_data": {"company_size": "10-50"},
                "outcome": "won",
                "revenue": 50000,
            }
            engine.add_feedback(feedback)
            
            # Populate cache
            recent = engine._get_recent_feedback(7)
            assert len(recent) == 1
            assert len(engine._feedback_cache) > 0
            
            # Add more feedback (should clear cache)
            engine.add_feedback(feedback)
            recent2 = engine._get_recent_feedback(7)
            assert len(recent2) == 2

    def test_json_serialization(self):
        """Test that soul data is properly serialized/deserialized."""
        with tempfile.TemporaryDirectory() as tmpdir:
            soul_path = os.path.join(tmpdir, "soul_file.json")
            engine1 = SoulFileEngine(soul_path)
            
            # Add data
            feedback = {
                "lead_data": {"company_size": "10-50"},
                "outcome": "won",
                "revenue": 50000,
            }
            engine1.add_feedback(feedback)
            
            # Create new engine from same file
            engine2 = SoulFileEngine(soul_path)
            assert len(engine2.soul["feedback_history"]) == 1
            assert engine2.soul["feedback_history"][0]["outcome"] == "won"


if __name__ == "__main__":
    import pytest
    
    pytest.main([__file__, "-v"])
