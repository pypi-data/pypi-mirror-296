import { g as F, w as d } from "./Index-DfZDcs7I.js";
const B = window.ms_globals.React, k = window.ms_globals.ReactDOM.createPortal, z = window.ms_globals.antd.theme, A = window.ms_globals.antd.Radio;
var E = {
  exports: {}
}, w = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var J = B, M = Symbol.for("react.element"), Y = Symbol.for("react.fragment"), G = Object.prototype.hasOwnProperty, H = J.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Q = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(l, t, r) {
  var o, s = {}, e = null, n = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (n = t.ref);
  for (o in t) G.call(t, o) && !Q.hasOwnProperty(o) && (s[o] = t[o]);
  if (l && l.defaultProps) for (o in t = l.defaultProps, t) s[o] === void 0 && (s[o] = t[o]);
  return {
    $$typeof: M,
    type: l,
    key: e,
    ref: n,
    props: s,
    _owner: H.current
  };
}
w.Fragment = Y;
w.jsx = j;
w.jsxs = j;
E.exports = w;
var V = E.exports;
const {
  SvelteComponent: X,
  assign: I,
  binding_callbacks: R,
  check_outros: Z,
  component_subscribe: x,
  compute_slots: $,
  create_slot: ee,
  detach: f,
  element: D,
  empty: te,
  exclude_internal_props: h,
  get_all_dirty_from_scope: se,
  get_slot_changes: oe,
  group_outros: ne,
  init: re,
  insert: p,
  safe_not_equal: le,
  set_custom_element_data: C,
  space: ae,
  transition_in: m,
  transition_out: g,
  update_slot_base: ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: ce,
  getContext: _e,
  onDestroy: ue,
  setContext: de
} = window.__gradio__svelte__internal;
function S(l) {
  let t, r;
  const o = (
    /*#slots*/
    l[7].default
  ), s = ee(
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
    m(e, n) {
      p(e, t, n), s && s.m(t, null), l[9](t), r = !0;
    },
    p(e, n) {
      s && s.p && (!r || n & /*$$scope*/
      64) && ie(
        s,
        o,
        e,
        /*$$scope*/
        e[6],
        r ? oe(
          o,
          /*$$scope*/
          e[6],
          n,
          null
        ) : se(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (m(s, e), r = !0);
    },
    o(e) {
      g(s, e), r = !1;
    },
    d(e) {
      e && f(t), s && s.d(e), l[9](null);
    }
  };
}
function fe(l) {
  let t, r, o, s, e = (
    /*$$slots*/
    l[4].default && S(l)
  );
  return {
    c() {
      t = D("react-portal-target"), r = ae(), e && e.c(), o = te(), C(t, "class", "svelte-1rt0kpf");
    },
    m(n, i) {
      p(n, t, i), l[8](t), p(n, r, i), e && e.m(n, i), p(n, o, i), s = !0;
    },
    p(n, [i]) {
      /*$$slots*/
      n[4].default ? e ? (e.p(n, i), i & /*$$slots*/
      16 && m(e, 1)) : (e = S(n), e.c(), m(e, 1), e.m(o.parentNode, o)) : e && (ne(), g(e, 1, 1, () => {
        e = null;
      }), Z());
    },
    i(n) {
      s || (m(e), s = !0);
    },
    o(n) {
      g(e), s = !1;
    },
    d(n) {
      n && (f(t), f(r), f(o)), l[8](null), e && e.d(n);
    }
  };
}
function O(l) {
  const {
    svelteInit: t,
    ...r
  } = l;
  return r;
}
function pe(l, t, r) {
  let o, s, {
    $$slots: e = {},
    $$scope: n
  } = t;
  const i = $(e);
  let {
    svelteInit: c
  } = t;
  const y = d(O(t)), _ = d();
  x(l, _, (a) => r(0, o = a));
  const u = d();
  x(l, u, (a) => r(1, s = a));
  const v = [], N = _e("$$ms-gr-antd-react-wrapper"), {
    slotKey: T,
    slotIndex: q,
    subSlotIndex: K
  } = F() || {}, L = c({
    parent: N,
    props: y,
    target: _,
    slot: u,
    slotKey: T,
    slotIndex: q,
    subSlotIndex: K,
    onDestroy(a) {
      v.push(a);
    }
  });
  de("$$ms-gr-antd-react-wrapper", L), ce(() => {
    y.set(O(t));
  }), ue(() => {
    v.forEach((a) => a());
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
  return l.$$set = (a) => {
    r(17, t = I(I({}, t), h(a))), "svelteInit" in a && r(5, c = a.svelteInit), "$$scope" in a && r(6, n = a.$$scope);
  }, t = h(t), [o, s, _, u, i, c, n, e, U, W];
}
class me extends X {
  constructor(t) {
    super(), re(this, t, pe, fe, le, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, b = window.ms_globals.tree;
function we(l) {
  function t(r) {
    const o = d(), s = new me({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const n = {
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
          }, i = e.parent ?? b;
          return i.nodes = [...i.nodes, n], P({
            createPortal: k,
            node: b
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== o), P({
              createPortal: k,
              node: b
            });
          }), n;
        },
        ...r.props
      }
    });
    return o.set(s), s;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const ge = we(({
  onValueChange: l,
  onChange: t,
  elRef: r,
  style: o,
  ...s
}) => {
  const {
    token: e
  } = z.useToken();
  return /* @__PURE__ */ V.jsx(A.Button, {
    ...s,
    style: {
      ...o,
      "--ms-gr-antd-line-width": e.lineWidth + "px"
    },
    ref: r,
    onChange: (n) => {
      t == null || t(n), l(n.target.checked);
    }
  });
});
export {
  ge as Radio,
  ge as default
};
