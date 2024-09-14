import { g as A, w as f } from "./Index-DMN2ShL-.js";
const j = window.ms_globals.React, k = window.ms_globals.ReactDOM.createPortal, B = window.ms_globals.antdIcons;
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
var J = j, M = Symbol.for("react.element"), Y = Symbol.for("react.fragment"), G = Object.prototype.hasOwnProperty, H = J.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Q = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(r, t, n) {
  var s, o = {}, e = null, l = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) G.call(t, s) && !Q.hasOwnProperty(s) && (o[s] = t[s]);
  if (r && r.defaultProps) for (s in t = r.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: M,
    type: r,
    key: e,
    ref: l,
    props: o,
    _owner: H.current
  };
}
g.Fragment = Y;
g.jsx = D;
g.jsxs = D;
C.exports = g;
var b = C.exports;
const {
  SvelteComponent: V,
  assign: x,
  binding_callbacks: h,
  check_outros: X,
  component_subscribe: R,
  compute_slots: Z,
  create_slot: $,
  detach: d,
  element: N,
  empty: ee,
  exclude_internal_props: S,
  get_all_dirty_from_scope: te,
  get_slot_changes: se,
  group_outros: ne,
  init: oe,
  insert: p,
  safe_not_equal: re,
  set_custom_element_data: q,
  space: le,
  transition_in: m,
  transition_out: y,
  update_slot_base: ae
} = window.__gradio__svelte__internal, {
  beforeUpdate: ce,
  getContext: ie,
  onDestroy: _e,
  setContext: ue
} = window.__gradio__svelte__internal;
function E(r) {
  let t, n;
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
      t = N("svelte-slot"), o && o.c(), q(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      p(e, t, l), o && o.m(t, null), r[9](t), n = !0;
    },
    p(e, l) {
      o && o.p && (!n || l & /*$$scope*/
      64) && ae(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        n ? se(
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
      n || (m(o, e), n = !0);
    },
    o(e) {
      y(o, e), n = !1;
    },
    d(e) {
      e && d(t), o && o.d(e), r[9](null);
    }
  };
}
function fe(r) {
  let t, n, s, o, e = (
    /*$$slots*/
    r[4].default && E(r)
  );
  return {
    c() {
      t = N("react-portal-target"), n = le(), e && e.c(), s = ee(), q(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      p(l, t, c), r[8](t), p(l, n, c), e && e.m(l, c), p(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && m(e, 1)) : (e = E(l), e.c(), m(e, 1), e.m(s.parentNode, s)) : e && (ne(), y(e, 1, 1, () => {
        e = null;
      }), X());
    },
    i(l) {
      o || (m(e), o = !0);
    },
    o(l) {
      y(e), o = !1;
    },
    d(l) {
      l && (d(t), d(n), d(s)), r[8](null), e && e.d(l);
    }
  };
}
function O(r) {
  const {
    svelteInit: t,
    ...n
  } = r;
  return n;
}
function de(r, t, n) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = Z(e);
  let {
    svelteInit: i
  } = t;
  const v = f(O(t)), _ = f();
  R(r, _, (a) => n(0, s = a));
  const u = f();
  R(r, u, (a) => n(1, o = a));
  const I = [], F = ie("$$ms-gr-antd-react-wrapper"), {
    slotKey: K,
    slotIndex: L,
    subSlotIndex: T
  } = A() || {}, U = i({
    parent: F,
    props: v,
    target: _,
    slot: u,
    slotKey: K,
    slotIndex: L,
    subSlotIndex: T,
    onDestroy(a) {
      I.push(a);
    }
  });
  ue("$$ms-gr-antd-react-wrapper", U), ce(() => {
    v.set(O(t));
  }), _e(() => {
    I.forEach((a) => a());
  });
  function W(a) {
    h[a ? "unshift" : "push"](() => {
      s = a, _.set(s);
    });
  }
  function z(a) {
    h[a ? "unshift" : "push"](() => {
      o = a, u.set(o);
    });
  }
  return r.$$set = (a) => {
    n(17, t = x(x({}, t), S(a))), "svelteInit" in a && n(5, i = a.svelteInit), "$$scope" in a && n(6, l = a.$$scope);
  }, t = S(t), [s, o, _, u, c, i, l, e, W, z];
}
class pe extends V {
  constructor(t) {
    super(), oe(this, t, de, fe, re, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, w = window.ms_globals.tree;
function me(r) {
  function t(n) {
    const s = f(), o = new pe({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
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
          }, c = e.parent ?? w;
          return c.nodes = [...c.nodes, l], P({
            createPortal: k,
            node: w
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), P({
              createPortal: k,
              node: w
            });
          }), l;
        },
        ...n.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const be = me(({
  name: r,
  Iconfont: t,
  ...n
}) => {
  const s = B[r];
  return /* @__PURE__ */ b.jsx(b.Fragment, {
    children: s ? j.createElement(s, n) : t ? /* @__PURE__ */ b.jsx(t, {
      type: r,
      ...n
    }) : null
  });
});
export {
  be as Icon,
  be as default
};
