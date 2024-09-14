import { g as z, w as f } from "./Index-Cqu3MFcO.js";
const W = window.ms_globals.React, I = window.ms_globals.ReactDOM.createPortal, A = window.ms_globals.antd.Flex;
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
function C(r, t, l) {
  var o, s = {}, e = null, n = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (n = t.ref);
  for (o in t) Y.call(t, o) && !H.hasOwnProperty(o) && (s[o] = t[o]);
  if (r && r.defaultProps) for (o in t = r.defaultProps, t) s[o] === void 0 && (s[o] = t[o]);
  return {
    $$typeof: J,
    type: r,
    key: e,
    ref: n,
    props: s,
    _owner: G.current
  };
}
b.Fragment = M;
b.jsx = C;
b.jsxs = C;
E.exports = b;
var Q = E.exports;
const {
  SvelteComponent: V,
  assign: k,
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
  const o = (
    /*#slots*/
    r[7].default
  ), s = $(
    o,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = j("svelte-slot"), s && s.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, n) {
      p(e, t, n), s && s.m(t, null), r[9](t), l = !0;
    },
    p(e, n) {
      s && s.p && (!l || n & /*$$scope*/
      64) && ae(
        s,
        o,
        e,
        /*$$scope*/
        e[6],
        l ? se(
          o,
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
      l || (m(s, e), l = !0);
    },
    o(e) {
      w(s, e), l = !1;
    },
    d(e) {
      e && d(t), s && s.d(e), r[9](null);
    }
  };
}
function fe(r) {
  let t, l, o, s, e = (
    /*$$slots*/
    r[4].default && h(r)
  );
  return {
    c() {
      t = j("react-portal-target"), l = le(), e && e.c(), o = ee(), D(t, "class", "svelte-1rt0kpf");
    },
    m(n, i) {
      p(n, t, i), r[8](t), p(n, l, i), e && e.m(n, i), p(n, o, i), s = !0;
    },
    p(n, [i]) {
      /*$$slots*/
      n[4].default ? e ? (e.p(n, i), i & /*$$slots*/
      16 && m(e, 1)) : (e = h(n), e.c(), m(e, 1), e.m(o.parentNode, o)) : e && (oe(), w(e, 1, 1, () => {
        e = null;
      }), X());
    },
    i(n) {
      s || (m(e), s = !0);
    },
    o(n) {
      w(e), s = !1;
    },
    d(n) {
      n && (d(t), d(l), d(o)), r[8](null), e && e.d(n);
    }
  };
}
function O(r) {
  const {
    svelteInit: t,
    ...l
  } = r;
  return l;
}
function de(r, t, l) {
  let o, s, {
    $$slots: e = {},
    $$scope: n
  } = t;
  const i = Z(e);
  let {
    svelteInit: c
  } = t;
  const v = f(O(t)), _ = f();
  R(r, _, (a) => l(0, o = a));
  const u = f();
  R(r, u, (a) => l(1, s = a));
  const y = [], F = ce("$$ms-gr-antd-react-wrapper"), {
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K
  } = z() || {}, L = c({
    parent: F,
    props: v,
    target: _,
    slot: u,
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K,
    onDestroy(a) {
      y.push(a);
    }
  });
  ue("$$ms-gr-antd-react-wrapper", L), ie(() => {
    v.set(O(t));
  }), _e(() => {
    y.forEach((a) => a());
  });
  function T(a) {
    x[a ? "unshift" : "push"](() => {
      o = a, _.set(o);
    });
  }
  function U(a) {
    x[a ? "unshift" : "push"](() => {
      s = a, u.set(s);
    });
  }
  return r.$$set = (a) => {
    l(17, t = k(k({}, t), S(a))), "svelteInit" in a && l(5, c = a.svelteInit), "$$scope" in a && l(6, n = a.$$scope);
  }, t = S(t), [o, s, _, u, i, c, n, e, T, U];
}
class pe extends V {
  constructor(t) {
    super(), ne(this, t, de, fe, re, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, g = window.ms_globals.tree;
function me(r) {
  function t(l) {
    const o = f(), s = new pe({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const n = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? g;
          return i.nodes = [...i.nodes, n], P({
            createPortal: I,
            node: g
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== o), P({
              createPortal: I,
              node: g
            });
          }), n;
        },
        ...l.props
      }
    });
    return o.set(s), s;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const ge = me((r) => /* @__PURE__ */ Q.jsx(A, {
  ...r
}));
export {
  ge as Flex,
  ge as default
};
