import { g as z, w as f } from "./Index-B0Jnm_Q_.js";
const U = window.ms_globals.React, W = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, A = window.ms_globals.antd.Progress;
var E = {
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
var B = U, J = Symbol.for("react.element"), Y = Symbol.for("react.fragment"), G = Object.prototype.hasOwnProperty, H = B.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Q = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function C(o, t, s) {
  var r, n = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t) G.call(t, r) && !Q.hasOwnProperty(r) && (n[r] = t[r]);
  if (o && o.defaultProps) for (r in t = o.defaultProps, t) n[r] === void 0 && (n[r] = t[r]);
  return {
    $$typeof: J,
    type: o,
    key: e,
    ref: l,
    props: n,
    _owner: H.current
  };
}
g.Fragment = Y;
g.jsx = C;
g.jsxs = C;
E.exports = g;
var V = E.exports;
const {
  SvelteComponent: X,
  assign: k,
  binding_callbacks: x,
  check_outros: Z,
  component_subscribe: P,
  compute_slots: $,
  create_slot: ee,
  detach: d,
  element: j,
  empty: te,
  exclude_internal_props: R,
  get_all_dirty_from_scope: oe,
  get_slot_changes: ne,
  group_outros: se,
  init: re,
  insert: p,
  safe_not_equal: le,
  set_custom_element_data: D,
  space: ae,
  transition_in: m,
  transition_out: b,
  update_slot_base: ce
} = window.__gradio__svelte__internal, {
  beforeUpdate: ie,
  getContext: ue,
  onDestroy: _e,
  setContext: fe
} = window.__gradio__svelte__internal;
function h(o) {
  let t, s;
  const r = (
    /*#slots*/
    o[7].default
  ), n = ee(
    r,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      t = j("svelte-slot"), n && n.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      p(e, t, l), n && n.m(t, null), o[9](t), s = !0;
    },
    p(e, l) {
      n && n.p && (!s || l & /*$$scope*/
      64) && ce(
        n,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? ne(
          r,
          /*$$scope*/
          e[6],
          l,
          null
        ) : oe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (m(n, e), s = !0);
    },
    o(e) {
      b(n, e), s = !1;
    },
    d(e) {
      e && d(t), n && n.d(e), o[9](null);
    }
  };
}
function de(o) {
  let t, s, r, n, e = (
    /*$$slots*/
    o[4].default && h(o)
  );
  return {
    c() {
      t = j("react-portal-target"), s = ae(), e && e.c(), r = te(), D(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      p(l, t, c), o[8](t), p(l, s, c), e && e.m(l, c), p(l, r, c), n = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && m(e, 1)) : (e = h(l), e.c(), m(e, 1), e.m(r.parentNode, r)) : e && (se(), b(e, 1, 1, () => {
        e = null;
      }), Z());
    },
    i(l) {
      n || (m(e), n = !0);
    },
    o(l) {
      b(e), n = !1;
    },
    d(l) {
      l && (d(t), d(s), d(r)), o[8](null), e && e.d(l);
    }
  };
}
function S(o) {
  const {
    svelteInit: t,
    ...s
  } = o;
  return s;
}
function pe(o, t, s) {
  let r, n, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = $(e);
  let {
    svelteInit: i
  } = t;
  const v = f(S(t)), u = f();
  P(o, u, (a) => s(0, r = a));
  const _ = f();
  P(o, _, (a) => s(1, n = a));
  const y = [], F = ue("$$ms-gr-antd-react-wrapper"), {
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K
  } = z() || {}, L = i({
    parent: F,
    props: v,
    target: u,
    slot: _,
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K,
    onDestroy(a) {
      y.push(a);
    }
  });
  fe("$$ms-gr-antd-react-wrapper", L), ie(() => {
    v.set(S(t));
  }), _e(() => {
    y.forEach((a) => a());
  });
  function M(a) {
    x[a ? "unshift" : "push"](() => {
      r = a, u.set(r);
    });
  }
  function T(a) {
    x[a ? "unshift" : "push"](() => {
      n = a, _.set(n);
    });
  }
  return o.$$set = (a) => {
    s(17, t = k(k({}, t), R(a))), "svelteInit" in a && s(5, i = a.svelteInit), "$$scope" in a && s(6, l = a.$$scope);
  }, t = R(t), [r, n, u, _, c, i, l, e, M, T];
}
class me extends X {
  constructor(t) {
    super(), re(this, t, pe, de, le, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, w = window.ms_globals.tree;
function ge(o) {
  function t(s) {
    const r = f(), n = new me({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? w;
          return c.nodes = [...c.nodes, l], O({
            createPortal: I,
            node: w
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), O({
              createPortal: I,
              node: w
            });
          }), l;
        },
        ...s.props
      }
    });
    return r.set(n), n;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
function we(o) {
  try {
    return typeof o == "string" ? new Function(`return (...args) => (${o})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function be(o) {
  return W(() => we(o), [o]);
}
const ye = ge(({
  format: o,
  ...t
}) => {
  const s = be(o);
  return /* @__PURE__ */ V.jsx(A, {
    ...t,
    format: s
  });
});
export {
  ye as Progress,
  ye as default
};
