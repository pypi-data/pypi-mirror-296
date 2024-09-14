import { g as z, w as d, c as A } from "./Index-YGugOdAP.js";
const B = window.ms_globals.React, W = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, i = window.ms_globals.antd.Layout;
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
var H = B, J = Symbol.for("react.element"), Y = Symbol.for("react.fragment"), G = Object.prototype.hasOwnProperty, Q = H.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, V = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(o, t, r) {
  var s, n = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) G.call(t, s) && !V.hasOwnProperty(s) && (n[s] = t[s]);
  if (o && o.defaultProps) for (s in t = o.defaultProps, t) n[s] === void 0 && (n[s] = t[s]);
  return {
    $$typeof: J,
    type: o,
    key: e,
    ref: l,
    props: n,
    _owner: Q.current
  };
}
w.Fragment = Y;
w.jsx = j;
w.jsxs = j;
E.exports = w;
var X = E.exports;
const {
  SvelteComponent: Z,
  assign: h,
  binding_callbacks: x,
  check_outros: $,
  component_subscribe: R,
  compute_slots: ee,
  create_slot: te,
  detach: m,
  element: D,
  empty: se,
  exclude_internal_props: S,
  get_all_dirty_from_scope: oe,
  get_slot_changes: ne,
  group_outros: re,
  init: le,
  insert: p,
  safe_not_equal: ae,
  set_custom_element_data: L,
  space: ue,
  transition_in: g,
  transition_out: y,
  update_slot_base: ce
} = window.__gradio__svelte__internal, {
  beforeUpdate: ie,
  getContext: _e,
  onDestroy: fe,
  setContext: de
} = window.__gradio__svelte__internal;
function C(o) {
  let t, r;
  const s = (
    /*#slots*/
    o[7].default
  ), n = te(
    s,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), n && n.c(), L(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      p(e, t, l), n && n.m(t, null), o[9](t), r = !0;
    },
    p(e, l) {
      n && n.p && (!r || l & /*$$scope*/
      64) && ce(
        n,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? ne(
          s,
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
      r || (g(n, e), r = !0);
    },
    o(e) {
      y(n, e), r = !1;
    },
    d(e) {
      e && m(t), n && n.d(e), o[9](null);
    }
  };
}
function me(o) {
  let t, r, s, n, e = (
    /*$$slots*/
    o[4].default && C(o)
  );
  return {
    c() {
      t = D("react-portal-target"), r = ue(), e && e.c(), s = se(), L(t, "class", "svelte-1rt0kpf");
    },
    m(l, u) {
      p(l, t, u), o[8](t), p(l, r, u), e && e.m(l, u), p(l, s, u), n = !0;
    },
    p(l, [u]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, u), u & /*$$slots*/
      16 && g(e, 1)) : (e = C(l), e.c(), g(e, 1), e.m(s.parentNode, s)) : e && (re(), y(e, 1, 1, () => {
        e = null;
      }), $());
    },
    i(l) {
      n || (g(e), n = !0);
    },
    o(l) {
      y(e), n = !1;
    },
    d(l) {
      l && (m(t), m(r), m(s)), o[8](null), e && e.d(l);
    }
  };
}
function O(o) {
  const {
    svelteInit: t,
    ...r
  } = o;
  return r;
}
function pe(o, t, r) {
  let s, n, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const u = ee(e);
  let {
    svelteInit: c
  } = t;
  const v = d(O(t)), _ = d();
  R(o, _, (a) => r(0, s = a));
  const f = d();
  R(o, f, (a) => r(1, n = a));
  const I = [], N = _e("$$ms-gr-antd-react-wrapper"), {
    slotKey: q,
    slotIndex: F,
    subSlotIndex: K
  } = z() || {}, M = c({
    parent: N,
    props: v,
    target: _,
    slot: f,
    slotKey: q,
    slotIndex: F,
    subSlotIndex: K,
    onDestroy(a) {
      I.push(a);
    }
  });
  de("$$ms-gr-antd-react-wrapper", M), ie(() => {
    v.set(O(t));
  }), fe(() => {
    I.forEach((a) => a());
  });
  function T(a) {
    x[a ? "unshift" : "push"](() => {
      s = a, _.set(s);
    });
  }
  function U(a) {
    x[a ? "unshift" : "push"](() => {
      n = a, f.set(n);
    });
  }
  return o.$$set = (a) => {
    r(17, t = h(h({}, t), S(a))), "svelteInit" in a && r(5, c = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, t = S(t), [s, n, _, f, u, c, l, e, T, U];
}
class ge extends Z {
  constructor(t) {
    super(), le(this, t, pe, me, ae, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, b = window.ms_globals.tree;
function we(o) {
  function t(r) {
    const s = d(), n = new ge({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, u = e.parent ?? b;
          return u.nodes = [...u.nodes, l], P({
            createPortal: k,
            node: b
          }), e.onDestroy(() => {
            u.nodes = u.nodes.filter((c) => c.svelteInstance !== s), P({
              createPortal: k,
              node: b
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(n), n;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const ye = we(({
  component: o,
  className: t,
  ...r
}) => {
  const s = W(() => {
    switch (o) {
      case "content":
        return i.Content;
      case "footer":
        return i.Footer;
      case "header":
        return i.Header;
      case "layout":
        return i;
      default:
        return i;
    }
  }, [o]);
  return /* @__PURE__ */ X.jsx(s, {
    ...r,
    className: A(t, o === "layout" ? null : `ms-gr-antd-layout-${o}`)
  });
});
export {
  ye as Base,
  ye as default
};
