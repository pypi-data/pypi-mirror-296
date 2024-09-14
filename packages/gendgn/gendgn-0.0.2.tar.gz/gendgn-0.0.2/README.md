# gendgn


## Development
### cd to the right folder 
```
cd gendgn/src
```

### execute pmtrz_wwr_constr.py
```
python -m gendgn.pmtrz_wwr_constr -i ../test_data/ifc/small_office.ifc -r ../results/json/pmtrz_wwr_constr.json
```

### execute sample_variants.py
```
python -m gendgn.sample_variants -n 5 -j ../results/json/pmtrz_wwr_constr.json
```

### execute exe_wwr_constr.py
```
python -m gendgn.exe_wwr_constr -j ../results/json/pmtrz_wwr_constr.json -i ../test_data/ifc/small_office.ifc -r ../results/ifc/small_office_variants
```

### execute batch_eval.py
```
python -m gendgn.batch_eval -v ../results/ifc/small_office_variants -r ../results/osmod/batch_small_offices -e ../test_data/epw/miami/USA_FL_Miami.Intl.AP.722020_TMY3.epw -d ../test_data/epw/miami/USA_FL_Miami.Intl.AP.722020_TMY3.ddy -m ../test_data/json/measure_sel.json
```