import unittest

import autograder.util.timestamp

class TestTimestamp(unittest.TestCase):
    def test_timestamp_conversions(self):
        # [(input, normal, pretty), ...]
        test_cases = [
            # Full information.
            ('2023-09-28T04:00:20Z', 1695873620000, '2023-09-28 04:00'),
            ('2023-09-28T04:00:20+00:00', 1695873620000, '2023-09-28 04:00'),
            ('2023-09-28T13:10:44+00:00', 1695906644000, '2023-09-28 13:10'),

            # Fractional seconds must be removed because of older python versions.
            ('2023-09-28T04:00:20.683684Z', 1695873620000, '2023-09-28 04:00'),
            ('2023-09-28T04:00:20.683684+00:00', 1695873620000, '2023-09-28 04:00'),
            ('2023-09-28T13:10:44.432050+00:00', 1695906644000, '2023-09-28 13:10'),
            ('2023-09-28T13:10:44.43205+00:00', 1695906644000, '2023-09-28 13:10'),

            # Unknown format.
            ('abc', '<Unknown Time (abc)>', '<Unknown Time (abc)>'),
        ]

        for i in range(len(test_cases)):
            (source, expected_normal, expected_pretty) = test_cases[i]

            first_normal_timestamp = autograder.util.timestamp.get(source,
                    pretty = False, adjust_tz = False)
            second_normal_timestamp = autograder.util.timestamp.get(first_normal_timestamp,
                    pretty = False, adjust_tz = False)

            self.assertEqual(expected_normal, first_normal_timestamp,
                    "Case %d: [%s] First Normal Timestamp" % (i, source))

            self.assertEqual(expected_normal, second_normal_timestamp,
                    "Case %d: [%s] Second Normal Timestamp" % (i, source))

            first_pretty_timestamp = autograder.util.timestamp.get(source,
                    pretty = True, adjust_tz = False)

            # Once created, pretty timestamps cannot be parsed (as they lack timezone information).

            self.assertEqual(expected_pretty, first_pretty_timestamp,
                    "Case %d: [%s] First Pretty Timestamp" % (i, source))

            # Converting from normal to pretty is possible, since no information is list.
            # In the other direction, timezone information is lost.
            normal_pretty_timestamp = autograder.util.timestamp.get(first_normal_timestamp,
                    pretty = True, adjust_tz = False)
            self.assertEqual(expected_pretty, normal_pretty_timestamp,
                    "Case %d: [%s] Normal Then Pretty Timestamp" % (i, source))
