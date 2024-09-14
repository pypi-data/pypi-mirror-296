import { g as z, w as f } from "./Index-B7ZTU07-.js";
const W = window.ms_globals.React, k = window.ms_globals.ReactDOM.createPortal, A = window.ms_globals.antd.Tag;
var E = {
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
var B = W, J = Symbol.for("react.element"), M = Symbol.for("react.fragment"), Y = Object.prototype.hasOwnProperty, G = B.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, H = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function T(n, t, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) Y.call(t, s) && !H.hasOwnProperty(s) && (o[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: J,
    type: n,
    key: e,
    ref: l,
    props: o,
    _owner: G.current
  };
}
b.Fragment = M;
b.jsx = T;
b.jsxs = T;
E.exports = b;
var Q = E.exports;
const {
  SvelteComponent: V,
  assign: I,
  binding_callbacks: x,
  check_outros: X,
  component_subscribe: R,
  compute_slots: Z,
  create_slot: $,
  detach: d,
  element: j,
  empty: ee,
  exclude_internal_props: S,
  get_all_dirty_from_scope: te,
  get_slot_changes: se,
  group_outros: oe,
  init: ne,
  insert: p,
  safe_not_equal: re,
  set_custom_element_data: C,
  space: le,
  transition_in: m,
  transition_out: w,
  update_slot_base: ae
} = window.__gradio__svelte__internal, {
  beforeUpdate: ce,
  getContext: ie,
  onDestroy: _e,
  setContext: ue
} = window.__gradio__svelte__internal;
function h(n) {
  let t, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = $(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = j("svelte-slot"), o && o.c(), C(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      p(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && ae(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? se(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : te(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (m(o, e), r = !0);
    },
    o(e) {
      w(o, e), r = !1;
    },
    d(e) {
      e && d(t), o && o.d(e), n[9](null);
    }
  };
}
function fe(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && h(n)
  );
  return {
    c() {
      t = j("react-portal-target"), r = le(), e && e.c(), s = ee(), C(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      p(l, t, c), n[8](t), p(l, r, c), e && e.m(l, c), p(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && m(e, 1)) : (e = h(l), e.c(), m(e, 1), e.m(s.parentNode, s)) : e && (oe(), w(e, 1, 1, () => {
        e = null;
      }), X());
    },
    i(l) {
      o || (m(e), o = !0);
    },
    o(l) {
      w(e), o = !1;
    },
    d(l) {
      l && (d(t), d(r), d(s)), n[8](null), e && e.d(l);
    }
  };
}
function O(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function de(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = Z(e);
  let {
    svelteInit: i
  } = t;
  const y = f(O(t)), _ = f();
  R(n, _, (a) => r(0, s = a));
  const u = f();
  R(n, u, (a) => r(1, o = a));
  const v = [], D = ie("$$ms-gr-antd-react-wrapper"), {
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K
  } = z() || {}, L = i({
    parent: D,
    props: y,
    target: _,
    slot: u,
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K,
    onDestroy(a) {
      v.push(a);
    }
  });
  ue("$$ms-gr-antd-react-wrapper", L), ce(() => {
    y.set(O(t));
  }), _e(() => {
    v.forEach((a) => a());
  });
  function U(a) {
    x[a ? "unshift" : "push"](() => {
      s = a, _.set(s);
    });
  }
  function F(a) {
    x[a ? "unshift" : "push"](() => {
      o = a, u.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = I(I({}, t), S(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, t = S(t), [s, o, _, u, c, i, l, e, U, F];
}
class pe extends V {
  constructor(t) {
    super(), ne(this, t, de, fe, re, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, g = window.ms_globals.tree;
function me(n) {
  function t(r) {
    const s = f(), o = new pe({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? g;
          return c.nodes = [...c.nodes, l], P({
            createPortal: k,
            node: g
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), P({
              createPortal: k,
              node: g
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const ge = me(({
  onChange: n,
  onValueChange: t,
  ...r
}) => /* @__PURE__ */ Q.jsx(A.CheckableTag, {
  ...r,
  onChange: (s) => {
    n == null || n(s), t(s);
  }
}));
export {
  ge as CheckableTag,
  ge as default
};
