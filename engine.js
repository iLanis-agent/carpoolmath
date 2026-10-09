/* Carpool math - exact arithmetic, labeled planning norms.
   Labeled norms shown in the UI: consumption 8 L per 100 km, workdays 5 per
   week, detour speed 40 km/h. Money rounds to 2 decimals, minutes to 1. */
(function (root) {
  'use strict';

  var L_PER_100 = 8, WORKDAYS = 5, DETOUR_KMH = 40;

  function num(v, name) {
    if (typeof v !== 'number' || !isFinite(v)) throw new Error(name + ' must be a number');
    return v;
  }
  function positive(v, name) {
    v = num(v, name);
    if (v <= 0) throw new Error(name + ' must be positive');
    return v;
  }
  function money(x) { return Math.round(x * 100) / 100; }
  function round1(x) { return Math.round(x * 10) / 10; }

  function tripSplit(kmOneWay, pricePerLiter, riders) {
    kmOneWay = positive(kmOneWay, 'distance');
    if (kmOneWay > 200) throw new Error('keep it under 200 km one-way (labeled)');
    pricePerLiter = positive(pricePerLiter, 'fuel price');
    if (pricePerLiter > 20) throw new Error('keep the fuel price under 20 (labeled)');
    riders = num(riders, 'riders');
    if (!Number.isInteger(riders)) throw new Error('count riders in whole people');
    if (riders < 2) throw new Error('a carpool needs at least 2 riders');
    if (riders > 7) throw new Error('keep it under 8 riders (labeled)');
    var total = money(kmOneWay * 2 / 100 * L_PER_100 * pricePerLiter);
    var perPerson = money(total / riders);
    var verdict = perPerson < 2 ? 'cheaper than the bus' : perPerson < 6 ? 'a fair split' : 'pricey - check the route';
    return { total: total, per_person: perPerson, verdict: verdict };
  }

  function rotation(drivers, weeks) {
    drivers = num(drivers, 'drivers');
    if (!Number.isInteger(drivers)) throw new Error('count drivers in whole people');
    if (drivers < 2) throw new Error('a rotation needs at least 2 drivers');
    if (drivers > 7) throw new Error('keep it under 8 drivers (labeled)');
    weeks = num(weeks, 'weeks');
    if (!Number.isInteger(weeks)) throw new Error('count weeks in whole weeks');
    if (weeks < 1) throw new Error('weeks must be positive');
    if (weeks > 52) throw new Error('keep it under 53 weeks (labeled)');
    var total = weeks * WORKDAYS;
    var base = Math.floor(total / drivers);
    var extra = total % drivers;
    var verdict = extra === 0 ? 'perfectly even' : extra + ' driver' + (extra === 1 ? '' : 's') + ' take' + (extra === 1 ? 's' : '') + ' one extra day';
    return { drives: total, min_drives: base, max_drives: extra === 0 ? base : base + 1, verdict: verdict };
  }

  function detour(kmOneWay, pricePerLiter, riders, detourKm) {
    kmOneWay = positive(kmOneWay, 'distance');
    if (kmOneWay > 200) throw new Error('keep it under 200 km one-way (labeled)');
    pricePerLiter = positive(pricePerLiter, 'fuel price');
    if (pricePerLiter > 20) throw new Error('keep the fuel price under 20 (labeled)');
    riders = num(riders, 'riders');
    if (!Number.isInteger(riders)) throw new Error('count riders in whole people');
    if (riders < 2) throw new Error('a carpool needs at least 2 riders');
    if (riders > 7) throw new Error('keep it under 8 riders (labeled)');
    detourKm = num(detourKm, 'detour');
    if (detourKm < 0) throw new Error('detour must be zero or more');
    if (detourKm > 50) throw new Error('keep the detour under 50 km (labeled)');
    var solo = money(kmOneWay * 2 / 100 * L_PER_100 * pricePerLiter);
    var shared = money((kmOneWay + detourKm) * 2 / 100 * L_PER_100 * pricePerLiter / riders);
    var saving = money(solo - shared);
    var detourMin = round1(detourKm * 2 / DETOUR_KMH * 60);
    var verdict = saving < 1 ? 'marginal - your call' : saving < 5 ? 'worth the detour' : 'a clear win';
    return { solo: solo, shared: shared, saving: saving, detour_min: detourMin, verdict: verdict };
  }

  var api = { tripSplit: tripSplit, rotation: rotation, detour: detour };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.CarpoolMath = api;
})(typeof window !== 'undefined' ? window : globalThis);
