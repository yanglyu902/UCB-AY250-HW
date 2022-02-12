# calcalc
This is a calculator for evaluating numerical expressions (in string format) both locally and on WolframAlpha. 

To install using pip: `pip install calcalc-toy`

### Usage 

After install, run
`from calcalc.CalCalc import calculate`

Example usage from the command line: 

`python CalCalc.py -s '2*sin(3)'`

`python CalCalc.py -w 'mass of the moon in kg'`

Alternative usage using python scripts/ipython:

`calculate('2*sin(3/5)+log(7)')`

`calculate('mass of the moon in kg', return_float=True, local=False)`

Notice: in order to query WolframAlpha, must use `local=False`. 

The query results can be displayed either in text or converted to float for further manipulation; this behavior is controled by the `return_float` parameter.  
