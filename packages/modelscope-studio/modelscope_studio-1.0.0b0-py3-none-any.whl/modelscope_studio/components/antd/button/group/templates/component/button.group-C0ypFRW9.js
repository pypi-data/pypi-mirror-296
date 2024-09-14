import { g as F, w as f } from "./Index-B0x4kV3I.js";
const W = window.ms_globals.React, k = window.ms_globals.ReactDOM.createPortal, G = window.ms_globals.antd.theme, z = window.ms_globals.antd.Button;
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
var A = W, J = Symbol.for("react.element"), M = Symbol.for("react.fragment"), Y = Object.prototype.hasOwnProperty, H = A.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Q = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function C(l, t, s) {
  var n, o = {}, e = null, r = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (n in t) Y.call(t, n) && !Q.hasOwnProperty(n) && (o[n] = t[n]);
  if (l && l.defaultProps) for (n in t = l.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: J,
    type: l,
    key: e,
    ref: r,
    props: o,
    _owner: H.current
  };
}
g.Fragment = M;
g.jsx = C;
g.jsxs = C;
E.exports = g;
var V = E.exports;
const {
  SvelteComponent: X,
  assign: I,
  binding_callbacks: h,
  check_outros: Z,
  component_subscribe: x,
  compute_slots: $,
  create_slot: ee,
  detach: d,
  element: j,
  empty: te,
  exclude_internal_props: R,
  get_all_dirty_from_scope: oe,
  get_slot_changes: se,
  group_outros: ne,
  init: re,
  insert: p,
  safe_not_equal: le,
  set_custom_element_data: D,
  space: ae,
  transition_in: m,
  transition_out: b,
  update_slot_base: ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: ue,
  getContext: ce,
  onDestroy: _e,
  setContext: fe
} = window.__gradio__svelte__internal;
function S(l) {
  let t, s;
  const n = (
    /*#slots*/
    l[7].default
  ), o = ee(
    n,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = j("svelte-slot"), o && o.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      p(e, t, r), o && o.m(t, null), l[9](t), s = !0;
    },
    p(e, r) {
      o && o.p && (!s || r & /*$$scope*/
      64) && ie(
        o,
        n,
        e,
        /*$$scope*/
        e[6],
        s ? se(
          n,
          /*$$scope*/
          e[6],
          r,
          null
        ) : oe(
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
      e && d(t), o && o.d(e), l[9](null);
    }
  };
}
function de(l) {
  let t, s, n, o, e = (
    /*$$slots*/
    l[4].default && S(l)
  );
  return {
    c() {
      t = j("react-portal-target"), s = ae(), e && e.c(), n = te(), D(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      p(r, t, i), l[8](t), p(r, s, i), e && e.m(r, i), p(r, n, i), o = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && m(e, 1)) : (e = S(r), e.c(), m(e, 1), e.m(n.parentNode, n)) : e && (ne(), b(e, 1, 1, () => {
        e = null;
      }), Z());
    },
    i(r) {
      o || (m(e), o = !0);
    },
    o(r) {
      b(e), o = !1;
    },
    d(r) {
      r && (d(t), d(s), d(n)), l[8](null), e && e.d(r);
    }
  };
}
function O(l) {
  const {
    svelteInit: t,
    ...s
  } = l;
  return s;
}
function pe(l, t, s) {
  let n, o, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const i = $(e);
  let {
    svelteInit: u
  } = t;
  const y = f(O(t)), c = f();
  x(l, c, (a) => s(0, n = a));
  const _ = f();
  x(l, _, (a) => s(1, o = a));
  const v = [], B = ce("$$ms-gr-antd-react-wrapper"), {
    slotKey: N,
    slotIndex: T,
    subSlotIndex: q
  } = F() || {}, K = u({
    parent: B,
    props: y,
    target: c,
    slot: _,
    slotKey: N,
    slotIndex: T,
    subSlotIndex: q,
    onDestroy(a) {
      v.push(a);
    }
  });
  fe("$$ms-gr-antd-react-wrapper", K), ue(() => {
    y.set(O(t));
  }), _e(() => {
    v.forEach((a) => a());
  });
  function L(a) {
    h[a ? "unshift" : "push"](() => {
      n = a, c.set(n);
    });
  }
  function U(a) {
    h[a ? "unshift" : "push"](() => {
      o = a, _.set(o);
    });
  }
  return l.$$set = (a) => {
    s(17, t = I(I({}, t), R(a))), "svelteInit" in a && s(5, u = a.svelteInit), "$$scope" in a && s(6, r = a.$$scope);
  }, t = R(t), [n, o, c, _, i, u, r, e, L, U];
}
class me extends X {
  constructor(t) {
    super(), re(this, t, pe, de, le, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, w = window.ms_globals.tree;
function ge(l) {
  function t(s) {
    const n = f(), o = new me({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? w;
          return i.nodes = [...i.nodes, r], P({
            createPortal: k,
            node: w
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((u) => u.svelteInstance !== n), P({
              createPortal: k,
              node: w
            });
          }), r;
        },
        ...s.props
      }
    });
    return n.set(o), o;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
const be = ge(({
  style: l,
  ...t
}) => {
  const {
    token: s
  } = G.useToken();
  return /* @__PURE__ */ V.jsx(z.Group, {
    ...t,
    style: {
      ...l,
      "--ms-gr-antd-line-width": s.lineWidth + "px"
    }
  });
});
export {
  be as ButtonGroup,
  be as default
};
