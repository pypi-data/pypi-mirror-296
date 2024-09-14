import { g as W, w as f } from "./Index-PQi0UtYN.js";
const T = window.ms_globals.React, U = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, z = window.ms_globals.antd.Affix;
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
var B = T, J = Symbol.for("react.element"), Y = Symbol.for("react.fragment"), G = Object.prototype.hasOwnProperty, H = B.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Q = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function C(n, t, s) {
  var r, o = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t) G.call(t, r) && !Q.hasOwnProperty(r) && (o[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: J,
    type: n,
    key: e,
    ref: l,
    props: o,
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
  component_subscribe: R,
  compute_slots: $,
  create_slot: ee,
  detach: d,
  element: j,
  empty: te,
  exclude_internal_props: h,
  get_all_dirty_from_scope: ne,
  get_slot_changes: oe,
  group_outros: se,
  init: re,
  insert: p,
  safe_not_equal: le,
  set_custom_element_data: D,
  space: ie,
  transition_in: m,
  transition_out: b,
  update_slot_base: ae
} = window.__gradio__svelte__internal, {
  beforeUpdate: ce,
  getContext: ue,
  onDestroy: _e,
  setContext: fe
} = window.__gradio__svelte__internal;
function S(n) {
  let t, s;
  const r = (
    /*#slots*/
    n[7].default
  ), o = ee(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = j("svelte-slot"), o && o.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      p(e, t, l), o && o.m(t, null), n[9](t), s = !0;
    },
    p(e, l) {
      o && o.p && (!s || l & /*$$scope*/
      64) && ae(
        o,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? oe(
          r,
          /*$$scope*/
          e[6],
          l,
          null
        ) : ne(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (m(o, e), s = !0);
    },
    o(e) {
      b(o, e), s = !1;
    },
    d(e) {
      e && d(t), o && o.d(e), n[9](null);
    }
  };
}
function de(n) {
  let t, s, r, o, e = (
    /*$$slots*/
    n[4].default && S(n)
  );
  return {
    c() {
      t = j("react-portal-target"), s = ie(), e && e.c(), r = te(), D(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      p(l, t, a), n[8](t), p(l, s, a), e && e.m(l, a), p(l, r, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && m(e, 1)) : (e = S(l), e.c(), m(e, 1), e.m(r.parentNode, r)) : e && (se(), b(e, 1, 1, () => {
        e = null;
      }), Z());
    },
    i(l) {
      o || (m(e), o = !0);
    },
    o(l) {
      b(e), o = !1;
    },
    d(l) {
      l && (d(t), d(s), d(r)), n[8](null), e && e.d(l);
    }
  };
}
function O(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function pe(n, t, s) {
  let r, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = $(e);
  let {
    svelteInit: c
  } = t;
  const v = f(O(t)), u = f();
  R(n, u, (i) => s(0, r = i));
  const _ = f();
  R(n, _, (i) => s(1, o = i));
  const y = [], F = ue("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: N,
    subSlotIndex: q
  } = W() || {}, K = c({
    parent: F,
    props: v,
    target: u,
    slot: _,
    slotKey: A,
    slotIndex: N,
    subSlotIndex: q,
    onDestroy(i) {
      y.push(i);
    }
  });
  fe("$$ms-gr-antd-react-wrapper", K), ce(() => {
    v.set(O(t));
  }), _e(() => {
    y.forEach((i) => i());
  });
  function L(i) {
    x[i ? "unshift" : "push"](() => {
      r = i, u.set(r);
    });
  }
  function M(i) {
    x[i ? "unshift" : "push"](() => {
      o = i, _.set(o);
    });
  }
  return n.$$set = (i) => {
    s(17, t = k(k({}, t), h(i))), "svelteInit" in i && s(5, c = i.svelteInit), "$$scope" in i && s(6, l = i.$$scope);
  }, t = h(t), [r, o, u, _, a, c, l, e, L, M];
}
class me extends X {
  constructor(t) {
    super(), re(this, t, pe, de, le, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, w = window.ms_globals.tree;
function ge(n) {
  function t(s) {
    const r = f(), o = new me({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? w;
          return a.nodes = [...a.nodes, l], P({
            createPortal: I,
            node: w
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== r), P({
              createPortal: I,
              node: w
            });
          }), l;
        },
        ...s.props
      }
    });
    return r.set(o), o;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
function we(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function be(n) {
  return U(() => we(n), [n]);
}
const ye = ge(({
  target: n,
  ...t
}) => {
  const s = be(n);
  return /* @__PURE__ */ V.jsx(z, {
    ...t,
    target: s
  });
});
export {
  ye as Affix,
  ye as default
};
