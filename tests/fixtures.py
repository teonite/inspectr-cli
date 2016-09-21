# -*- coding: utf-8 -*-
from textwrap import dedent


flake8_output = dedent("""\
    apps/core/sensitivity_analysis.py:129:1: R701  'analyse_sensitivity' is too complex (44)
    apps/core/signals.py:18:1: R701  'updateNpvFromProject' is too complex (23)
    apps/core/utils.py:15:1: R701  'floatify' is too complex (19)
    apps/core/utils.py:116:1: R701  'duplicate' is too complex (22)
    apps/export/views.py:182:1: R701  'PortfolioPDFView' is too complex (14)
    apps/export/views.py:193:5: R701  'get_context_data' is too complex (14)

    """)

unittest_output = dedent("""\
    .F
    ======================================================================
    FAIL: test_npv (apps.core.tests.TestIndices)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/core/apps/core/tests.py", line 340, in test_npv
        self.assertAlmostEqual(npv, Decimal(self.index_results['npv']), 2)
    AssertionError: Decimal('158.60223620475019773') != Decimal('157') within 2 places

    ----------------------------------------------------------------------
    Ran 2 tests in 0.368s

    FAILED (failures=1)
    """)

coverage_output = dedent("""\
    Name                                                                                                  Stmts   Miss  Cover
    -------------------------------------------------------------------------------------------------------------------------
    conf/loggersettings.py                                                                                   11      4    64%
    tools/manage.py                                                                                           8      0   100%
    -------------------------------------------------------------------------------------------------------------------------
    TOTAL                                                                                                  4572   1673    63%
    """)

coverage_output_small = dedent("""\
    Name           Stmts   Miss  Cover
    ----------------------------------
    __init__.py        0      0   100%
    inspectr.py       16     16     0%
    parsers.py        43      0   100%
    reporters.py      21     21     0%
    utils.py          60     60     0%
    ----------------------------------
    TOTAL            140     97    31%
    """)

eslint_output = dedent("""\
    /home/jck/workspace/work/teonite/azoty/web-app/src/ng-app/app.js
    1:1   warning  Rule 'generator-star' was removed and replaced by: generator-star-spacing    generator-star
    50:32  error    'defaultLanguage' is not defined                                             no-undef

    ✖ 47 problems (5 errors, 42 warnings)

    """)

eslint_output_noerrors = dedent("""\
    """)

eslint_output_custom = dedent("""\
    > react-boilerplate@3.0.0 lint:js /home/user/workspace/project
    > eslint .


""")


jasmine_output = dedent("""\
    26 06 2016 12:12:55.610:WARN [watcher]: Pattern "/home/jck/workspace/work/teonite/azoty/web-app/node_modules/sinon/pkg/sinon-timers.js" does not match any file.
    26 06 2016 12:12:55.618:WARN [watcher]: Pattern "/home/jck/workspace/work/teonite/azoty/web-app/dist/lib/angularjs/angular-locale_en-gb.js" does not match any file.
    26 06 2016 12:12:56.434:INFO [karma]: Karma v1.0.0 server started at http://localhost:9876/
    26 06 2016 12:12:56.434:INFO [launcher]: Launching browser PhantomJS with unlimited concurrency
    26 06 2016 12:12:56.440:INFO [launcher]: Starting browser PhantomJS
    26 06 2016 12:12:56.665:INFO [PhantomJS 2.1.1 (Linux 0.0.0)]: Connected on socket /#IoRwzZfZzsf3BNGbAAAA with id 9818241
    PhantomJS 2.1.1 (Linux 0.0.0): Executed 1 of 1 SUCCESS (0.206 secs / 0 secs)
    -------------------|----------|----------|----------|----------|----------------|
    File               |  % Stmts | % Branch |  % Funcs |  % Lines |Uncovered Lines |
    -------------------|----------|----------|----------|----------|----------------|
     js/               |     1.85 |        0 |        0 |     1.85 |                |
      app.js           |     1.85 |        0 |        0 |     1.85 |... 700,701,705 |
     js/ng-app/        |     4.63 |     0.54 |     1.08 |     4.72 |                |
      cms.js           |     4.63 |     0.54 |     1.08 |     4.72 |... 10554,10556 |
     js/portfolio-app/ |     6.06 |        0 |        0 |      6.1 |                |
      portfolio.js     |     6.06 |        0 |        0 |      6.1 |... 6,2433,2438 |
    -------------------|----------|----------|----------|----------|----------------|
    All files          |     4.82 |     0.43 |     0.78 |     4.91 |                |
    -------------------|----------|----------|----------|----------|----------------|


    """)

jasmine_output_integers = dedent("""\
    26 06 2016 12:12:55.610:WARN [watcher]: Pattern "/home/jck/workspace/work/teonite/azoty/web-app/node_modules/sinon/pkg/sinon-timers.js" does not match any file.
    26 06 2016 12:12:55.618:WARN [watcher]: Pattern "/home/jck/workspace/work/teonite/azoty/web-app/dist/lib/angularjs/angular-locale_en-gb.js" does not match any file.
    26 06 2016 12:12:56.434:INFO [karma]: Karma v1.0.0 server started at http://localhost:9876/
    26 06 2016 12:12:56.434:INFO [launcher]: Launching browser PhantomJS with unlimited concurrency
    26 06 2016 12:12:56.440:INFO [launcher]: Starting browser PhantomJS
    26 06 2016 12:12:56.665:INFO [PhantomJS 2.1.1 (Linux 0.0.0)]: Connected on socket /#IoRwzZfZzsf3BNGbAAAA with id 9818241
    PhantomJS 2.1.1 (Linux 0.0.0): Executed 1 of 1 SUCCESS (0.206 secs / 0 secs)
    -------------------|----------|----------|----------|----------|----------------|
    File               |  % Stmts | % Branch |  % Funcs |  % Lines |Uncovered Lines |
    -------------------|----------|----------|----------|----------|----------------|
     js/               |     1.85 |        0 |        0 |     1.85 |                |
      app.js           |     1.85 |        0 |        0 |     1.85 |... 700,701,705 |
     js/ng-app/        |     4.63 |     0.54 |     1.08 |     4.72 |                |
      cms.js           |     4.63 |     0.54 |     1.08 |     4.72 |... 10554,10556 |
     js/portfolio-app/ |     6.06 |        0 |        0 |      6.1 |                |
      portfolio.js     |     6.06 |        0 |        0 |      6.1 |... 6,2433,2438 |
    -------------------|----------|----------|----------|----------|----------------|
     All files         |      100 |      100 |      100 |      100 |                |
    -------------------|----------|----------|----------|----------|----------------|


    """)


mocha_success_output = dedent("""\
    02 07 2016 09:19:45.773:INFO [PhantomJS 2.1.1 (Linux 0.0.0)]: Connected on socket /#VePfZy9E04WvElXUAAAA with id 13721294
      selectLocationState
        ✔ should select the route as a plain JS object
      hooks
        getHooks
          ✔ given a store, should return all hooks
        helpers
          injectAsyncReducer
            ✔ given a store, it should provide a function to inject a reducer
          injectAsyncSagas
            ✔ given a store, it should provide a function to inject a saga

    =============================== Coverage summary ===============================
    Statements   : 85.31% ( 604/708 ), 54 ignored
    Branches     : 88.66% ( 258/291 ), 94 ignored
    Functions    : 73.86% ( 113/153 ), 22 ignored
    Lines        : 77.25% ( 258/334 )
    ================================================================================

    Finished in 0.08 secs / 0.034 secs

    SUMMARY:
    ✔ 4 tests completed

    """)


mocha_fail_output = dedent("""\
    Finished in 0.095 secs / 0.039 secs

    SUMMARY:
    ✔ 3 tests completed
    ✖ 1 test failed

    """)

karma_coverage_summary_line = "All files          |     4.82 |     0.43 |     0.78 |     4.91 |                |"
jasmine_summary_success_line = "PhantomJS 2.1.1 (Linux 0.0.0): Executed 1 of 1 SUCCESS (0.205 secs / 0.001 secs)"
jasmine_summary_fail_line = "PhantomJS 2.1.1 (Linux 0.0.0): Executed 1 of 1 (1 FAILED) ERROR (0.21 secs / 0.001 secs)"

pytest_output_fail = dedent("""\
    __________________________________________________________________________________________ test_coverage_pytest_reporter ___________________________________________________________________________________________

    monkeypatch = <_pytest.monkeypatch.monkeypatch object at 0x7f7fd9b752e8>

        def test_coverage_pytest_reporter(monkeypatch):
            monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    >       report = coverage_pytest_reporter({}, [])
    E       NameError: name 'coverage_pytest_reporter' is not defined

    tests/test_reporters.py:80: NameError
    ======================================================================================= 4 failed, 38 passed in 0.10 seconds ========================================================================================
    """)

pytest_output_success = dedent("""\
    =============================================================================================== test session starts ================================================================================================
    platform linux -- Python 3.5.1, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
    rootdir: /home/jck/workspace/work/teonite/inspectr/inspectr/inspectr, inifile:
    plugins: mock-1.1
    collected 21 items

    tests/test_utils.py .....................

    ============================================================================================ 21 passed in 0.05 seconds =============================================================================================
    """)


radon_maintainability_output = dedent("""\
    apps/api/mixins.py - A
    apps/api/serializers.py - B
    apps/api/tests.py - A
    apps/api/index_views.py - A
    apps/api/__init__.py - A
    apps/api/urls.py - A
    apps/api/excel_exporter.py - B
    apps/api/model_views.py - C
    apps/api/portfolio_util.py - C
    apps/api/admin.py - A
    """)


radon_cyclomatic_complexity_output = dedent("""\
    inspectr/main.py
        F 36:0 run - B
        F 31:0 get_datetime - A
    inspectr/utils.py
        F 13:0 validate_and_parse_config - B
        F 38:0 init_db - A
        F 28:0 validate_connector_config - A
        F 77:0 print_command - A
        F 60:0 save_report - A
        F 73:0 colored - A
        F 84:0 print_command_ok - A
        F 91:0 print_command_fail - A
    inspectr/executor.py
        F 11:0 decode - A
        F 22:0 execute - A
        F 5:0 clean - A
    """)


coffeelint_output = dedent("""\
    ✗ src/app/services/GenericCaseActions.coffee
       ✗ #32: Line exceeds maximum allowed length. Length is 88, max is 80.
    ✓ src/app/services/LawyerProfile.coffee
    ✓ src/app/services/VersionFactory.coffee
    ✗ src/app/services/VindicationCase.coffee
       ✗ #6: Line exceeds maximum allowed length. Length is 82, max is 80.

    ✗ Lint! » 98 errors and 0 warnings in 41 files

    """)

tslint_output = dedent("""\
    src/app/views/personalization/step3.ts[18, 13]: The selector of the component "PersonalizationStep3View" should be named kebab-case (https://goo.gl/mBg67Z)
    src/app/views/personalization/step3.ts[17, 1]: Implement lifecycle hook interfaces (https://goo.gl/w1Nwk3)
    src/app/views/personalization/step3.ts[23, 14]: The name of the class PersonalizationStep3View should end with the suffix Component (https://goo.gl/5X1TE7)
    src/app/views/start.ts[2, 9]: Unused import: 'ActivatedRoute'
    src/app/views/start.ts[1, 25]: " should be '
    src/app/views/start.ts[2, 38]: " should be '
    """)
