import { g as z, w as f } from "./Index-fJdvfd2P.js";
const W = window.ms_globals.React, I = window.ms_globals.ReactDOM.createPortal, A = window.ms_globals.antd.Radio;
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
function j(l, t, n) {
  var o, s = {}, e = null, r = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (o in t) Y.call(t, o) && !H.hasOwnProperty(o) && (s[o] = t[o]);
  if (l && l.defaultProps) for (o in t = l.defaultProps, t) s[o] === void 0 && (s[o] = t[o]);
  return {
    $$typeof: J,
    type: l,
    key: e,
    ref: r,
    props: s,
    _owner: G.current
  };
}
b.Fragment = M;
b.jsx = j;
b.jsxs = j;
E.exports = b;
var Q = E.exports;
const {
  SvelteComponent: V,
  assign: k,
  binding_callbacks: R,
  check_outros: X,
  component_subscribe: x,
  compute_slots: Z,
  create_slot: $,
  detach: d,
  element: D,
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
  transition_out: g,
  update_slot_base: ae
} = window.__gradio__svelte__internal, {
  beforeUpdate: ie,
  getContext: ce,
  onDestroy: _e,
  setContext: ue
} = window.__gradio__svelte__internal;
function O(l) {
  let t, n;
  const o = (
    /*#slots*/
    l[7].default
  ), s = $(
    o,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), s && s.c(), C(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      p(e, t, r), s && s.m(t, null), l[9](t), n = !0;
    },
    p(e, r) {
      s && s.p && (!n || r & /*$$scope*/
      64) && ae(
        s,
        o,
        e,
        /*$$scope*/
        e[6],
        n ? se(
          o,
          /*$$scope*/
          e[6],
          r,
          null
        ) : te(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (m(s, e), n = !0);
    },
    o(e) {
      g(s, e), n = !1;
    },
    d(e) {
      e && d(t), s && s.d(e), l[9](null);
    }
  };
}
function fe(l) {
  let t, n, o, s, e = (
    /*$$slots*/
    l[4].default && O(l)
  );
  return {
    c() {
      t = D("react-portal-target"), n = le(), e && e.c(), o = ee(), C(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      p(r, t, i), l[8](t), p(r, n, i), e && e.m(r, i), p(r, o, i), s = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && m(e, 1)) : (e = O(r), e.c(), m(e, 1), e.m(o.parentNode, o)) : e && (oe(), g(e, 1, 1, () => {
        e = null;
      }), X());
    },
    i(r) {
      s || (m(e), s = !0);
    },
    o(r) {
      g(e), s = !1;
    },
    d(r) {
      r && (d(t), d(n), d(o)), l[8](null), e && e.d(r);
    }
  };
}
function P(l) {
  const {
    svelteInit: t,
    ...n
  } = l;
  return n;
}
function de(l, t, n) {
  let o, s, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const i = Z(e);
  let {
    svelteInit: c
  } = t;
  const v = f(P(t)), _ = f();
  x(l, _, (a) => n(0, o = a));
  const u = f();
  x(l, u, (a) => n(1, s = a));
  const y = [], N = ce("$$ms-gr-antd-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: L
  } = z() || {}, T = c({
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
  ue("$$ms-gr-antd-react-wrapper", T), ie(() => {
    v.set(P(t));
  }), _e(() => {
    y.forEach((a) => a());
  });
  function U(a) {
    R[a ? "unshift" : "push"](() => {
      o = a, _.set(o);
    });
  }
  function F(a) {
    R[a ? "unshift" : "push"](() => {
      s = a, u.set(s);
    });
  }
  return l.$$set = (a) => {
    n(17, t = k(k({}, t), S(a))), "svelteInit" in a && n(5, c = a.svelteInit), "$$scope" in a && n(6, r = a.$$scope);
  }, t = S(t), [o, s, _, u, i, c, r, e, U, F];
}
class pe extends V {
  constructor(t) {
    super(), ne(this, t, de, fe, re, {
      svelteInit: 5
    });
  }
}
const h = window.ms_globals.rerender, w = window.ms_globals.tree;
function me(l) {
  function t(n) {
    const o = f(), s = new pe({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? w;
          return i.nodes = [...i.nodes, r], h({
            createPortal: I,
            node: w
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== o), h({
              createPortal: I,
              node: w
            });
          }), r;
        },
        ...n.props
      }
    });
    return o.set(s), s;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const we = me(({
  onValueChange: l,
  onChange: t,
  elRef: n,
  ...o
}) => /* @__PURE__ */ Q.jsx(A, {
  ...o,
  ref: n,
  onChange: (s) => {
    t == null || t(s), l(s.target.checked);
  }
}));
export {
  we as Radio,
  we as default
};
