import unittest

from agents.context.context_manager import ConversationContext


class TestConversationContext(unittest.TestCase):

    def test_update_and_get(self):
        context = ConversationContext()

        context.update({
            "location": "Kochi",
            "date": "tomorrow",
            "activity": "fishing",
        })

        self.assertEqual(
            context.get(),
            {
                "location": "Kochi",
                "date": "tomorrow",
                "time": None,
                "activity": "fishing",
            },
        )

    def test_fill_missing_entities(self):
        context = ConversationContext()

        context.update({
            "location": "Kochi",
            "date": "tomorrow",
            "activity": "fishing",
        })

        result = context.fill_missing({
            "location": None,
            "date": None,
            "time": "morning",
            "activity": None,
        })

        self.assertEqual(result["location"], "Kochi")
        self.assertEqual(result["date"], "tomorrow")
        self.assertEqual(result["time"], "morning")
        self.assertEqual(result["activity"], "fishing")

    def test_current_query_overrides_context(self):
        context = ConversationContext()

        context.update({
            "location": "Kochi",
            "activity": "fishing",
        })

        result = context.fill_missing({
            "location": "Mumbai",
            "activity": None,
        })

        self.assertEqual(result["location"], "Mumbai")
        self.assertEqual(result["activity"], "fishing")

    def test_clear(self):
        context = ConversationContext()

        context.update({
            "location": "Kochi",
            "date": "tomorrow",
        })

        context.clear()

        self.assertEqual(
            context.get(),
            {
                "location": None,
                "date": None,
                "time": None,
                "activity": None,
            },
        )


if __name__ == "__main__":
    unittest.main()
