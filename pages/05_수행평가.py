IndexError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/ai-project/pages/05_수행평가.py", line 125, in <module>
    main()
    ~~~~^^
File "/mount/src/ai-project/pages/05_수행평가.py", line 108, in main
    fig = create_plotly_bar_chart(top_10_stations)
File "/mount/src/ai-project/pages/05_수행평가.py", line 64, in create_plotly_bar_chart
    df_top10['color'] = df_top10['순위'].apply(lambda x: color_list[x])
                        ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/core/series.py", line 4943, in apply
    ).apply()
      ~~~~~^^
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/core/apply.py", line 1422, in apply
    return self.apply_standard()
           ~~~~~~~~~~~~~~~~~~~^^
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/core/apply.py", line 1502, in apply_standard
    mapped = obj._map_values(
        mapper=curried, na_action=action, convert=self.convert_dtype
    )
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/core/base.py", line 925, in _map_values
    return algorithms.map_array(arr, mapper, na_action=na_action, convert=convert)
           ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/core/algorithms.py", line 1743, in map_array
    return lib.map_infer(values, mapper, convert=convert)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "pandas/_libs/lib.pyx", line 2999, in pandas._libs.lib.map_infer
File "/mount/src/ai-project/pages/05_수행평가.py", line 64, in <lambda>
    df_top10['color'] = df_top10['순위'].apply(lambda x: color_list[x])
                                                         ~~~~~~~~~~^^^
