import { g as M, w as m } from "./Index-CBMzs1de.js";
const P = window.ms_globals.React, G = window.ms_globals.React.forwardRef, H = window.ms_globals.React.useRef, K = window.ms_globals.React.useEffect, v = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Button;
var L = {
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
var Y = P, Q = Symbol.for("react.element"), V = Symbol.for("react.fragment"), X = Object.prototype.hasOwnProperty, Z = Y.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, $ = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(n, t, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (r in t) X.call(t, r) && !$.hasOwnProperty(r) && (l[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: Q,
    type: n,
    key: e,
    ref: o,
    props: l,
    _owner: Z.current
  };
}
b.Fragment = V;
b.jsx = j;
b.jsxs = j;
L.exports = b;
var E = L.exports;
const {
  SvelteComponent: ee,
  assign: x,
  binding_callbacks: I,
  check_outros: te,
  component_subscribe: C,
  compute_slots: ne,
  create_slot: oe,
  detach: p,
  element: N,
  empty: re,
  exclude_internal_props: R,
  get_all_dirty_from_scope: se,
  get_slot_changes: le,
  group_outros: ie,
  init: ce,
  insert: g,
  safe_not_equal: ae,
  set_custom_element_data: D,
  space: ue,
  transition_in: w,
  transition_out: y,
  update_slot_base: de
} = window.__gradio__svelte__internal, {
  beforeUpdate: fe,
  getContext: _e,
  onDestroy: me,
  setContext: pe
} = window.__gradio__svelte__internal;
function S(n) {
  let t, s;
  const r = (
    /*#slots*/
    n[7].default
  ), l = oe(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = N("svelte-slot"), l && l.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      g(e, t, o), l && l.m(t, null), n[9](t), s = !0;
    },
    p(e, o) {
      l && l.p && (!s || o & /*$$scope*/
      64) && de(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? le(
          r,
          /*$$scope*/
          e[6],
          o,
          null
        ) : se(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (w(l, e), s = !0);
    },
    o(e) {
      y(l, e), s = !1;
    },
    d(e) {
      e && p(t), l && l.d(e), n[9](null);
    }
  };
}
function ge(n) {
  let t, s, r, l, e = (
    /*$$slots*/
    n[4].default && S(n)
  );
  return {
    c() {
      t = N("react-portal-target"), s = ue(), e && e.c(), r = re(), D(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      g(o, t, i), n[8](t), g(o, s, i), e && e.m(o, i), g(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && w(e, 1)) : (e = S(o), e.c(), w(e, 1), e.m(r.parentNode, r)) : e && (ie(), y(e, 1, 1, () => {
        e = null;
      }), te());
    },
    i(o) {
      l || (w(e), l = !0);
    },
    o(o) {
      y(e), l = !1;
    },
    d(o) {
      o && (p(t), p(s), p(r)), n[8](null), e && e.d(o);
    }
  };
}
function k(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function we(n, t, s) {
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const i = ne(e);
  let {
    svelteInit: d
  } = t;
  const _ = m(k(t)), c = m();
  C(n, c, (a) => s(0, r = a));
  const u = m();
  C(n, u, (a) => s(1, l = a));
  const f = [], z = _e("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: B,
    subSlotIndex: F
  } = M() || {}, T = d({
    parent: z,
    props: _,
    target: c,
    slot: u,
    slotKey: A,
    slotIndex: B,
    subSlotIndex: F,
    onDestroy(a) {
      f.push(a);
    }
  });
  pe("$$ms-gr-antd-react-wrapper", T), fe(() => {
    _.set(k(t));
  }), me(() => {
    f.forEach((a) => a());
  });
  function U(a) {
    I[a ? "unshift" : "push"](() => {
      r = a, c.set(r);
    });
  }
  function q(a) {
    I[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return n.$$set = (a) => {
    s(17, t = x(x({}, t), R(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, o = a.$$scope);
  }, t = R(t), [r, l, c, u, i, d, o, e, U, q];
}
class be extends ee {
  constructor(t) {
    super(), ce(this, t, we, ge, ae, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, h = window.ms_globals.tree;
function he(n) {
  function t(s) {
    const r = m(), l = new be({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
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
          }, i = e.parent ?? h;
          return i.nodes = [...i.nodes, o], O({
            createPortal: v,
            node: h
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), O({
              createPortal: v,
              node: h
            });
          }), o;
        },
        ...s.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
const ye = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ve(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const r = n[s];
    return typeof r == "number" && !ye.includes(s) ? t[s] = r + "px" : t[s] = r, t;
  }, {}) : {};
}
function W(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: e,
      type: o,
      useCapture: i
    }) => {
      t.addEventListener(o, e, i);
    });
  });
  const s = Array.from(n.children);
  for (let r = 0; r < s.length; r++) {
    const l = s[r], e = W(l);
    t.replaceChild(e, t.children[r]);
  }
  return t;
}
function Ee(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const xe = G(({
  slot: n,
  clone: t,
  className: s,
  style: r
}, l) => {
  const e = H();
  return K(() => {
    var _;
    if (!e.current || !n)
      return;
    let o = n;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ee(l, c), s && c.classList.add(...s.split(" ")), r) {
        const u = ve(r);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var u;
        o = W(n), o.style.display = "contents", i(), (u = e.current) == null || u.appendChild(o);
      };
      c(), d = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(o) && ((f = e.current) == null || f.removeChild(o)), c();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (_ = e.current) == null || _.appendChild(o);
    return () => {
      var c, u;
      o.style.display = "", (c = e.current) != null && c.contains(o) && ((u = e.current) == null || u.removeChild(o)), d == null || d.disconnect();
    };
  }, [n, t, s, r, l]), P.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), Ce = he(({
  slots: n,
  ...t
}) => /* @__PURE__ */ E.jsx(J, {
  ...t,
  icon: n.icon ? /* @__PURE__ */ E.jsx(xe, {
    slot: n.icon
  }) : t.icon
}));
export {
  Ce as Button,
  Ce as default
};
