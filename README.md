# Carpool math

Three carpool-planning calculators as a small static site - exact arithmetic,
every borrowed number labeled:

- **Trip split** - one-way distance, fuel price and riders become the round
  trip's fuel cost (labeled 8 L/100 km) and the split per person.
- **Rotation planner** - drivers and weeks become drives each (labeled 5
  workdays per week), and who takes the extra day.
- **Detour check** - solo cost versus shared cost with the pickup detour
  (labeled 40 km/h), the saving and the minutes.

## Files

- `index.html` - landing page
- `app.html` - the three calculators
- `engine.js` - all arithmetic, shared by the page and the tests
- `oracle.py` - independent Python mirror of the engine; regenerates `expected.json`
- `expected.json` - 48 cases (per-card values plus error cases)
- `test.js` - runs the engine against `expected.json` (node test.js)

## Tests

```
python3 oracle.py   # regenerate expected cases
node test.js        # engine vs oracle
```
