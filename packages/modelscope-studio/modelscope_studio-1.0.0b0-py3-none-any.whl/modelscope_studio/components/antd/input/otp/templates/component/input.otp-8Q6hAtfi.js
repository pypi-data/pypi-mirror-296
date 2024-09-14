import { g as z, w as f } from "./Index-CEftDEUh.js";
const U = window.ms_globals.React, W = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, A = window.ms_globals.antd.Input;
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
var B = U, J = Symbol.for("react.element"), Y = Symbol.for("react.fragment"), G = Object.prototype.hasOwnProperty, H = B.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Q = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(n, t, s) {
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
w.Fragment = Y;
w.jsx = j;
w.jsxs = j;
E.exports = w;
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
  element: D,
  empty: te,
  exclude_internal_props: O,
  get_all_dirty_from_scope: ne,
  get_slot_changes: oe,
  group_outros: se,
  init: re,
  insert: p,
  safe_not_equal: le,
  set_custom_element_data: F,
  space: ue,
  transition_in: m,
  transition_out: g,
  update_slot_base: ce
} = window.__gradio__svelte__internal, {
  beforeUpdate: ie,
  getContext: ae,
  onDestroy: _e,
  setContext: fe
} = window.__gradio__svelte__internal;
function P(n) {
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
      t = D("svelte-slot"), o && o.c(), F(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      p(e, t, l), o && o.m(t, null), n[9](t), s = !0;
    },
    p(e, l) {
      o && o.p && (!s || l & /*$$scope*/
      64) && ce(
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
      g(o, e), s = !1;
    },
    d(e) {
      e && d(t), o && o.d(e), n[9](null);
    }
  };
}
function de(n) {
  let t, s, r, o, e = (
    /*$$slots*/
    n[4].default && P(n)
  );
  return {
    c() {
      t = D("react-portal-target"), s = ue(), e && e.c(), r = te(), F(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      p(l, t, c), n[8](t), p(l, s, c), e && e.m(l, c), p(l, r, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && m(e, 1)) : (e = P(l), e.c(), m(e, 1), e.m(r.parentNode, r)) : e && (se(), g(e, 1, 1, () => {
        e = null;
      }), Z());
    },
    i(l) {
      o || (m(e), o = !0);
    },
    o(l) {
      g(e), o = !1;
    },
    d(l) {
      l && (d(t), d(s), d(r)), n[8](null), e && e.d(l);
    }
  };
}
function S(n) {
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
  const c = $(e);
  let {
    svelteInit: i
  } = t;
  const y = f(S(t)), a = f();
  R(n, a, (u) => s(0, r = u));
  const _ = f();
  R(n, _, (u) => s(1, o = u));
  const v = [], T = ae("$$ms-gr-antd-react-wrapper"), {
    slotKey: C,
    slotIndex: N,
    subSlotIndex: q
  } = z() || {}, K = i({
    parent: T,
    props: y,
    target: a,
    slot: _,
    slotKey: C,
    slotIndex: N,
    subSlotIndex: q,
    onDestroy(u) {
      v.push(u);
    }
  });
  fe("$$ms-gr-antd-react-wrapper", K), ie(() => {
    y.set(S(t));
  }), _e(() => {
    v.forEach((u) => u());
  });
  function L(u) {
    x[u ? "unshift" : "push"](() => {
      r = u, a.set(r);
    });
  }
  function M(u) {
    x[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return n.$$set = (u) => {
    s(17, t = k(k({}, t), O(u))), "svelteInit" in u && s(5, i = u.svelteInit), "$$scope" in u && s(6, l = u.$$scope);
  }, t = O(t), [r, o, a, _, c, i, l, e, L, M];
}
class me extends X {
  constructor(t) {
    super(), re(this, t, pe, de, le, {
      svelteInit: 5
    });
  }
}
const h = window.ms_globals.rerender, b = window.ms_globals.tree;
function we(n) {
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
          }, c = e.parent ?? b;
          return c.nodes = [...c.nodes, l], h({
            createPortal: I,
            node: b
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), h({
              createPortal: I,
              node: b
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
function be(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function ge(n) {
  return W(() => be(n), [n]);
}
const ve = we(({
  formatter: n,
  onValueChange: t,
  onChange: s,
  elRef: r,
  ...o
}) => {
  const e = ge(n);
  return /* @__PURE__ */ V.jsx(A.OTP, {
    ...o,
    ref: r,
    formatter: e,
    onChange: (l) => {
      s == null || s(l), t(l);
    }
  });
});
export {
  ve as InputOTP,
  ve as default
};
