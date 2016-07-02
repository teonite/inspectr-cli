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

karma_output = dedent("""\
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

karma_coverage_summary_line = "All files          |     4.82 |     0.43 |     0.78 |     4.91 |                |"
karma_summary_success_line = "PhantomJS 2.1.1 (Linux 0.0.0): Executed 1 of 1 SUCCESS (0.205 secs / 0.001 secs)"
karma_summary_fail_line = "PhantomJS 2.1.1 (Linux 0.0.0): Executed 1 of 1 (1 FAILED) ERROR (0.21 secs / 0.001 secs)"

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
