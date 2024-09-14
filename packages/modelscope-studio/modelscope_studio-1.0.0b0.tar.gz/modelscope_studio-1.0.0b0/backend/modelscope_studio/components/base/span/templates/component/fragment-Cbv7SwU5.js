import { g as A, w as f } from "./Index-DXnzSG5c.js";
const z = window.ms_globals.React, I = window.ms_globals.ReactDOM.createPortal;
var C = {
  exports: {}
}, g = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var B = z, J = Symbol.for("react.element"), M = Symbol.for("react.fragment"), Y = Object.prototype.hasOwnProperty, G = B.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, H = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(r, t, l) {
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
g.Fragment = M;
g.jsx = j;
g.jsxs = j;
C.exports = g;
var k = C.exports;
const {
  SvelteComponent: Q,
  assign: x,
  binding_callbacks: R,
  check_outros: V,
  component_subscribe: S,
  compute_slots: X,
  create_slot: Z,
  detach: d,
  element: D,
  empty: $,
  exclude_internal_props: h,
  get_all_dirty_from_scope: ee,
  get_slot_changes: te,
  group_outros: se,
  init: oe,
  insert: p,
  safe_not_equal: ne,
  set_custom_element_data: F,
  space: re,
  transition_in: m,
  transition_out: w,
  update_slot_base: le
} = window.__gradio__svelte__internal, {
  beforeUpdate: ae,
  getContext: ie,
  onDestroy: ce,
  setContext: _e
} = window.__gradio__svelte__internal;
function O(r) {
  let t, l;
  const o = (
    /*#slots*/
    r[7].default
  ), s = Z(
    o,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), s && s.c(), F(t, "class", "svelte-1rt0kpf");
    },
    m(e, n) {
      p(e, t, n), s && s.m(t, null), r[9](t), l = !0;
    },
    p(e, n) {
      s && s.p && (!l || n & /*$$scope*/
      64) && le(
        s,
        o,
        e,
        /*$$scope*/
        e[6],
        l ? te(
          o,
          /*$$scope*/
          e[6],
          n,
          null
        ) : ee(
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
function ue(r) {
  let t, l, o, s, e = (
    /*$$slots*/
    r[4].default && O(r)
  );
  return {
    c() {
      t = D("react-portal-target"), l = re(), e && e.c(), o = $(), F(t, "class", "svelte-1rt0kpf");
    },
    m(n, i) {
      p(n, t, i), r[8](t), p(n, l, i), e && e.m(n, i), p(n, o, i), s = !0;
    },
    p(n, [i]) {
      /*$$slots*/
      n[4].default ? e ? (e.p(n, i), i & /*$$slots*/
      16 && m(e, 1)) : (e = O(n), e.c(), m(e, 1), e.m(o.parentNode, o)) : e && (se(), w(e, 1, 1, () => {
        e = null;
      }), V());
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
function P(r) {
  const {
    svelteInit: t,
    ...l
  } = r;
  return l;
}
function fe(r, t, l) {
  let o, s, {
    $$slots: e = {},
    $$scope: n
  } = t;
  const i = X(e);
  let {
    svelteInit: c
  } = t;
  const v = f(P(t)), _ = f();
  S(r, _, (a) => l(0, o = a));
  const u = f();
  S(r, u, (a) => l(1, s = a));
  const y = [], N = ie("$$ms-gr-antd-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: L
  } = A() || {}, T = c({
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
  _e("$$ms-gr-antd-react-wrapper", T), ae(() => {
    v.set(P(t));
  }), ce(() => {
    y.forEach((a) => a());
  });
  function U(a) {
    R[a ? "unshift" : "push"](() => {
      o = a, _.set(o);
    });
  }
  function W(a) {
    R[a ? "unshift" : "push"](() => {
      s = a, u.set(s);
    });
  }
  return r.$$set = (a) => {
    l(17, t = x(x({}, t), h(a))), "svelteInit" in a && l(5, c = a.svelteInit), "$$scope" in a && l(6, n = a.$$scope);
  }, t = h(t), [o, s, _, u, i, c, n, e, U, W];
}
class de extends Q {
  constructor(t) {
    super(), oe(this, t, fe, ue, ne, {
      svelteInit: 5
    });
  }
}
const E = window.ms_globals.rerender, b = window.ms_globals.tree;
function pe(r) {
  function t(l) {
    const o = f(), s = new de({
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
          }, i = e.parent ?? b;
          return i.nodes = [...i.nodes, n], E({
            createPortal: I,
            node: b
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== o), E({
              createPortal: I,
              node: b
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
const ge = pe(({
  children: r
}) => /* @__PURE__ */ k.jsx(k.Fragment, {
  children: r
}));
export {
  ge as Fragment,
  ge as default
};
