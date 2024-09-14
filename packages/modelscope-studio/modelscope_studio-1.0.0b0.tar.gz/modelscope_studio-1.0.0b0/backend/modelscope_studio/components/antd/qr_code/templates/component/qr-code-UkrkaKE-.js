import { g as W, w as f } from "./Index-ZVODuxZ3.js";
const F = window.ms_globals.React, I = window.ms_globals.ReactDOM.createPortal, z = window.ms_globals.antd.QRCode;
var P = {
  exports: {}
}, b = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var A = F, B = Symbol.for("react.element"), J = Symbol.for("react.fragment"), M = Object.prototype.hasOwnProperty, Y = A.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, G = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function E(r, t, l) {
  var s, o = {}, e = null, n = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (n = t.ref);
  for (s in t) M.call(t, s) && !G.hasOwnProperty(s) && (o[s] = t[s]);
  if (r && r.defaultProps) for (s in t = r.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: B,
    type: r,
    key: e,
    ref: n,
    props: o,
    _owner: Y.current
  };
}
b.Fragment = J;
b.jsx = E;
b.jsxs = E;
P.exports = b;
var H = P.exports;
const {
  SvelteComponent: V,
  assign: k,
  binding_callbacks: R,
  check_outros: X,
  component_subscribe: x,
  compute_slots: Z,
  create_slot: $,
  detach: d,
  element: j,
  empty: ee,
  exclude_internal_props: S,
  get_all_dirty_from_scope: te,
  get_slot_changes: oe,
  group_outros: se,
  init: ne,
  insert: p,
  safe_not_equal: re,
  set_custom_element_data: D,
  space: le,
  transition_in: m,
  transition_out: w,
  update_slot_base: ae
} = window.__gradio__svelte__internal, {
  beforeUpdate: ie,
  getContext: ce,
  onDestroy: _e,
  setContext: ue
} = window.__gradio__svelte__internal;
function h(r) {
  let t, l;
  const s = (
    /*#slots*/
    r[7].default
  ), o = $(
    s,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = j("svelte-slot"), o && o.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, n) {
      p(e, t, n), o && o.m(t, null), r[9](t), l = !0;
    },
    p(e, n) {
      o && o.p && (!l || n & /*$$scope*/
      64) && ae(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        l ? oe(
          s,
          /*$$scope*/
          e[6],
          n,
          null
        ) : te(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      l || (m(o, e), l = !0);
    },
    o(e) {
      w(o, e), l = !1;
    },
    d(e) {
      e && d(t), o && o.d(e), r[9](null);
    }
  };
}
function fe(r) {
  let t, l, s, o, e = (
    /*$$slots*/
    r[4].default && h(r)
  );
  return {
    c() {
      t = j("react-portal-target"), l = le(), e && e.c(), s = ee(), D(t, "class", "svelte-1rt0kpf");
    },
    m(n, i) {
      p(n, t, i), r[8](t), p(n, l, i), e && e.m(n, i), p(n, s, i), o = !0;
    },
    p(n, [i]) {
      /*$$slots*/
      n[4].default ? e ? (e.p(n, i), i & /*$$slots*/
      16 && m(e, 1)) : (e = h(n), e.c(), m(e, 1), e.m(s.parentNode, s)) : e && (se(), w(e, 1, 1, () => {
        e = null;
      }), X());
    },
    i(n) {
      o || (m(e), o = !0);
    },
    o(n) {
      w(e), o = !1;
    },
    d(n) {
      n && (d(t), d(l), d(s)), r[8](null), e && e.d(n);
    }
  };
}
function C(r) {
  const {
    svelteInit: t,
    ...l
  } = r;
  return l;
}
function de(r, t, l) {
  let s, o, {
    $$slots: e = {},
    $$scope: n
  } = t;
  const i = Z(e);
  let {
    svelteInit: c
  } = t;
  const v = f(C(t)), _ = f();
  x(r, _, (a) => l(0, s = a));
  const u = f();
  x(r, u, (a) => l(1, o = a));
  const y = [], N = ce("$$ms-gr-antd-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: L
  } = W() || {}, Q = c({
    parent: N,
    props: v,
    target: _,
    slot: u,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: L,
    onDestroy(a) {
      y.push(a);
    }
  });
  ue("$$ms-gr-antd-react-wrapper", Q), ie(() => {
    v.set(C(t));
  }), _e(() => {
    y.forEach((a) => a());
  });
  function T(a) {
    R[a ? "unshift" : "push"](() => {
      s = a, _.set(s);
    });
  }
  function U(a) {
    R[a ? "unshift" : "push"](() => {
      o = a, u.set(o);
    });
  }
  return r.$$set = (a) => {
    l(17, t = k(k({}, t), S(a))), "svelteInit" in a && l(5, c = a.svelteInit), "$$scope" in a && l(6, n = a.$$scope);
  }, t = S(t), [s, o, _, u, i, c, n, e, T, U];
}
class pe extends V {
  constructor(t) {
    super(), ne(this, t, de, fe, re, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, g = window.ms_globals.tree;
function me(r) {
  function t(l) {
    const s = f(), o = new pe({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const n = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? g;
          return i.nodes = [...i.nodes, n], O({
            createPortal: I,
            node: g
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), O({
              createPortal: I,
              node: g
            });
          }), n;
        },
        ...l.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const ge = me(({
  ...r
}) => /* @__PURE__ */ H.jsx(z, {
  ...r
}));
export {
  ge as QRCode,
  ge as default
};
