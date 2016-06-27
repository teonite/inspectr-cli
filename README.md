# Adding reporters

1. Add reporter_required_settings and default_settings for your reporter in utils.py
2. Implement validation logic for your reporter in utils.parse_and_validate_config
3. Implement reporter in reporters.py - should invoke command, gather output and parse it with appropriate parser
4. Implement parser for command invoked by your reporter. Parser should return dictionary with keys:
* output - should contain command output split into lines (['output line 1', 'output line 2', ...])
* summary - contains relevant summary statistics from your reporter ({tests_executed: 10, tests_failed: 3})
5. Don't forget to test reporter, parser and validation (test_reporters, test_parsers, test_utils)
