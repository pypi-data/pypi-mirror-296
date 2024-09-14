import { g as z, w as v } from "./Index-DLQ7SMh7.js";
const W = window.ms_globals.React, b = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, B = window.ms_globals.antd.Calendar, D = window.ms_globals.dayjs;
var N = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var J = W, Y = Symbol.for("react.element"), G = Symbol.for("react.fragment"), H = Object.prototype.hasOwnProperty, Q = J.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, X = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(s, t, l) {
  var n, o = {}, e = null, r = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (n in t) H.call(t, n) && !X.hasOwnProperty(n) && (o[n] = t[n]);
  if (s && s.defaultProps) for (n in t = s.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: Y,
    type: s,
    key: e,
    ref: r,
    props: o,
    _owner: Q.current
  };
}
I.Fragment = G;
I.jsx = q;
I.jsxs = q;
N.exports = I;
var Z = N.exports;
const {
  SvelteComponent: $,
  assign: j,
  binding_callbacks: E,
  check_outros: ee,
  component_subscribe: S,
  compute_slots: te,
  create_slot: se,
  detach: w,
  element: A,
  empty: oe,
  exclude_internal_props: F,
  get_all_dirty_from_scope: ne,
  get_slot_changes: re,
  group_outros: le,
  init: ae,
  insert: y,
  safe_not_equal: ie,
  set_custom_element_data: K,
  space: ue,
  transition_in: g,
  transition_out: x,
  update_slot_base: ce
} = window.__gradio__svelte__internal, {
  beforeUpdate: _e,
  getContext: fe,
  onDestroy: de,
  setContext: pe
} = window.__gradio__svelte__internal;
function P(s) {
  let t, l;
  const n = (
    /*#slots*/
    s[7].default
  ), o = se(
    n,
    s,
    /*$$scope*/
    s[6],
    null
  );
  return {
    c() {
      t = A("svelte-slot"), o && o.c(), K(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      y(e, t, r), o && o.m(t, null), s[9](t), l = !0;
    },
    p(e, r) {
      o && o.p && (!l || r & /*$$scope*/
      64) && ce(
        o,
        n,
        e,
        /*$$scope*/
        e[6],
        l ? re(
          n,
          /*$$scope*/
          e[6],
          r,
          null
        ) : ne(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      l || (g(o, e), l = !0);
    },
    o(e) {
      x(o, e), l = !1;
    },
    d(e) {
      e && w(t), o && o.d(e), s[9](null);
    }
  };
}
function me(s) {
  let t, l, n, o, e = (
    /*$$slots*/
    s[4].default && P(s)
  );
  return {
    c() {
      t = A("react-portal-target"), l = ue(), e && e.c(), n = oe(), K(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      y(r, t, i), s[8](t), y(r, l, i), e && e.m(r, i), y(r, n, i), o = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && g(e, 1)) : (e = P(r), e.c(), g(e, 1), e.m(n.parentNode, n)) : e && (le(), x(e, 1, 1, () => {
        e = null;
      }), ee());
    },
    i(r) {
      o || (g(e), o = !0);
    },
    o(r) {
      x(e), o = !1;
    },
    d(r) {
      r && (w(t), w(l), w(n)), s[8](null), e && e.d(r);
    }
  };
}
function h(s) {
  const {
    svelteInit: t,
    ...l
  } = s;
  return l;
}
function be(s, t, l) {
  let n, o, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const i = te(e);
  let {
    svelteInit: c
  } = t;
  const p = v(h(t)), f = v();
  S(s, f, (a) => l(0, n = a));
  const d = v();
  S(s, d, (a) => l(1, o = a));
  const m = [], u = fe("$$ms-gr-antd-react-wrapper"), {
    slotKey: _,
    slotIndex: L,
    subSlotIndex: M
  } = z() || {}, T = c({
    parent: u,
    props: p,
    target: f,
    slot: d,
    slotKey: _,
    slotIndex: L,
    subSlotIndex: M,
    onDestroy(a) {
      m.push(a);
    }
  });
  pe("$$ms-gr-antd-react-wrapper", T), _e(() => {
    p.set(h(t));
  }), de(() => {
    m.forEach((a) => a());
  });
  function U(a) {
    E[a ? "unshift" : "push"](() => {
      n = a, f.set(n);
    });
  }
  function V(a) {
    E[a ? "unshift" : "push"](() => {
      o = a, d.set(o);
    });
  }
  return s.$$set = (a) => {
    l(17, t = j(j({}, t), F(a))), "svelteInit" in a && l(5, c = a.svelteInit), "$$scope" in a && l(6, r = a.$$scope);
  }, t = F(t), [n, o, f, d, i, c, r, e, U, V];
}
class ve extends $ {
  constructor(t) {
    super(), ae(this, t, be, me, ie, {
      svelteInit: 5
    });
  }
}
const C = window.ms_globals.rerender, k = window.ms_globals.tree;
function we(s) {
  function t(l) {
    const n = v(), o = new ve({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: s,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? k;
          return i.nodes = [...i.nodes, r], C({
            createPortal: R,
            node: k
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== n), C({
              createPortal: R,
              node: k
            });
          }), r;
        },
        ...l.props
      }
    });
    return n.set(o), o;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
function ye(s) {
  try {
    return typeof s == "string" ? new Function(`return (...args) => (${s})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function ge(s) {
  return b(() => ye(s), [s]);
}
function O(s) {
  return D(typeof s == "number" ? s * 1e3 : s);
}
const ke = we(({
  disabledDate: s,
  value: t,
  defaultValue: l,
  validRange: n,
  onChange: o,
  onPanelChange: e,
  onSelect: r,
  onValueChange: i,
  ...c
}) => {
  const p = ge(s), f = b(() => t ? O(t) : void 0, [t]), d = b(() => l ? O(l) : void 0, [l]), m = b(() => Array.isArray(n) ? n.map((u) => O(u)) : void 0, [n]);
  return /* @__PURE__ */ Z.jsx(B, {
    ...c,
    value: f,
    defaultValue: d,
    validRange: m,
    disabledDate: p,
    onChange: (u, ..._) => {
      i(u.valueOf() / 1e3), o == null || o(u.valueOf() / 1e3, ..._);
    },
    onPanelChange: (u, ..._) => {
      e == null || e(u.valueOf() / 1e3, ..._);
    },
    onSelect: (u, ..._) => {
      r == null || r(u.valueOf() / 1e3, ..._);
    }
  });
});
export {
  ke as Calendar,
  ke as default
};
