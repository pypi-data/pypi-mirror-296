import { g as Q, w as m } from "./Index-BJi3U3Lr.js";
const F = window.ms_globals.React, K = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useEffect, Y = window.ms_globals.React.useMemo, C = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Popover;
var L = {
  exports: {}
}, h = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var X = F, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function N(t, n, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (r in n) ee.call(n, r) && !ne.hasOwnProperty(r) && (l[r] = n[r]);
  if (t && t.defaultProps) for (r in n = t.defaultProps, n) l[r] === void 0 && (l[r] = n[r]);
  return {
    $$typeof: Z,
    type: t,
    key: e,
    ref: o,
    props: l,
    _owner: te.current
  };
}
h.Fragment = $;
h.jsx = N;
h.jsxs = N;
L.exports = h;
var p = L.exports;
const {
  SvelteComponent: oe,
  assign: x,
  binding_callbacks: E,
  check_outros: re,
  component_subscribe: I,
  compute_slots: se,
  create_slot: le,
  detach: g,
  element: D,
  empty: ie,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ae,
  group_outros: ue,
  init: de,
  insert: w,
  safe_not_equal: fe,
  set_custom_element_data: M,
  space: _e,
  transition_in: b,
  transition_out: y,
  update_slot_base: pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: me,
  getContext: ge,
  onDestroy: we,
  setContext: be
} = window.__gradio__svelte__internal;
function O(t) {
  let n, s;
  const r = (
    /*#slots*/
    t[7].default
  ), l = le(
    r,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = D("svelte-slot"), l && l.c(), M(n, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      w(e, n, o), l && l.m(n, null), t[9](n), s = !0;
    },
    p(e, o) {
      l && l.p && (!s || o & /*$$scope*/
      64) && pe(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? ae(
          r,
          /*$$scope*/
          e[6],
          o,
          null
        ) : ce(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (b(l, e), s = !0);
    },
    o(e) {
      y(l, e), s = !1;
    },
    d(e) {
      e && g(n), l && l.d(e), t[9](null);
    }
  };
}
function he(t) {
  let n, s, r, l, e = (
    /*$$slots*/
    t[4].default && O(t)
  );
  return {
    c() {
      n = D("react-portal-target"), s = _e(), e && e.c(), r = ie(), M(n, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      w(o, n, i), t[8](n), w(o, s, i), e && e.m(o, i), w(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = O(o), e.c(), b(e, 1), e.m(r.parentNode, r)) : e && (ue(), y(e, 1, 1, () => {
        e = null;
      }), re());
    },
    i(o) {
      l || (b(e), l = !0);
    },
    o(o) {
      y(e), l = !1;
    },
    d(o) {
      o && (g(n), g(s), g(r)), t[8](null), e && e.d(o);
    }
  };
}
function S(t) {
  const {
    svelteInit: n,
    ...s
  } = t;
  return s;
}
function ve(t, n, s) {
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = n;
  const i = se(e);
  let {
    svelteInit: d
  } = n;
  const _ = m(S(n)), c = m();
  I(t, c, (a) => s(0, r = a));
  const u = m();
  I(t, u, (a) => s(1, l = a));
  const f = [], z = ge("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U
  } = Q() || {}, q = d({
    parent: z,
    props: _,
    target: c,
    slot: u,
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U,
    onDestroy(a) {
      f.push(a);
    }
  });
  be("$$ms-gr-antd-react-wrapper", q), me(() => {
    _.set(S(n));
  }), we(() => {
    f.forEach((a) => a());
  });
  function G(a) {
    E[a ? "unshift" : "push"](() => {
      r = a, c.set(r);
    });
  }
  function H(a) {
    E[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return t.$$set = (a) => {
    s(17, n = x(x({}, n), R(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, o = a.$$scope);
  }, n = R(n), [r, l, c, u, i, d, o, e, G, H];
}
class ye extends oe {
  constructor(n) {
    super(), de(this, n, ve, he, fe, {
      svelteInit: 5
    });
  }
}
const k = window.ms_globals.rerender, v = window.ms_globals.tree;
function Ce(t) {
  function n(s) {
    const r = m(), l = new ye({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? v;
          return i.nodes = [...i.nodes, o], k({
            createPortal: C,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), k({
              createPortal: C,
              node: v
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
      s(n);
    });
  });
}
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ee(t) {
  return t ? Object.keys(t).reduce((n, s) => {
    const r = t[s];
    return typeof r == "number" && !xe.includes(s) ? n[s] = r + "px" : n[s] = r, n;
  }, {}) : {};
}
function W(t) {
  const n = t.cloneNode(!0);
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: e,
      type: o,
      useCapture: i
    }) => {
      n.addEventListener(o, e, i);
    });
  });
  const s = Array.from(t.children);
  for (let r = 0; r < s.length; r++) {
    const l = s[r], e = W(l);
    n.replaceChild(e, n.children[r]);
  }
  return n;
}
function Ie(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const P = K(({
  slot: t,
  clone: n,
  className: s,
  style: r
}, l) => {
  const e = B();
  return J(() => {
    var _;
    if (!e.current || !t)
      return;
    let o = t;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ie(l, c), s && c.classList.add(...s.split(" ")), r) {
        const u = Ee(r);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var u;
        o = W(t), o.style.display = "contents", i(), (u = e.current) == null || u.appendChild(o);
      };
      c(), d = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(o) && ((f = e.current) == null || f.removeChild(o)), c();
      }), d.observe(t, {
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
  }, [t, n, s, r, l]), F.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Re(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function j(t) {
  return Y(() => Re(t), [t]);
}
const Se = Ce(({
  slots: t,
  afterOpenChange: n,
  getPopupContainer: s,
  children: r,
  ...l
}) => {
  const e = j(n), o = j(s);
  return /* @__PURE__ */ p.jsx(p.Fragment, {
    children: /* @__PURE__ */ p.jsx(V, {
      ...l,
      afterOpenChange: e,
      getPopupContainer: o,
      title: t.title ? /* @__PURE__ */ p.jsx(P, {
        slot: t.title
      }) : l.title,
      content: t.content ? /* @__PURE__ */ p.jsx(P, {
        slot: t.content
      }) : l.content,
      children: r
    })
  });
});
export {
  Se as Popover,
  Se as default
};
