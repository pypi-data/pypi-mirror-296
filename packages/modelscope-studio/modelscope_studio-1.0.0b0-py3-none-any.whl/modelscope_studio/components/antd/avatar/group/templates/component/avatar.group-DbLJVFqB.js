import { g as Q, w as g, d as X, a as m } from "./Index-Cs1ZnT-w.js";
const S = window.ms_globals.React, A = window.ms_globals.React.useMemo, J = window.ms_globals.React.useState, N = window.ms_globals.React.useEffect, V = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, E = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Avatar;
var D = {
  exports: {}
}, x = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $ = S, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, oe = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(n, t, r) {
  var s, l = {}, e = null, o = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (s in t) ne.call(t, s) && !re.hasOwnProperty(s) && (l[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) l[s] === void 0 && (l[s] = t[s]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: o,
    props: l,
    _owner: oe.current
  };
}
x.Fragment = te;
x.jsx = F;
x.jsxs = F;
D.exports = x;
var _ = D.exports;
const {
  SvelteComponent: se,
  assign: C,
  binding_callbacks: R,
  check_outros: le,
  component_subscribe: k,
  compute_slots: ie,
  create_slot: ae,
  detach: v,
  element: G,
  empty: ce,
  exclude_internal_props: O,
  get_all_dirty_from_scope: ue,
  get_slot_changes: de,
  group_outros: fe,
  init: pe,
  insert: w,
  safe_not_equal: _e,
  set_custom_element_data: M,
  space: me,
  transition_in: b,
  transition_out: I,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: we,
  onDestroy: be,
  setContext: xe
} = window.__gradio__svelte__internal;
function j(n) {
  let t, r;
  const s = (
    /*#slots*/
    n[7].default
  ), l = ae(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = G("svelte-slot"), l && l.c(), M(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      w(e, t, o), l && l.m(t, null), n[9](t), r = !0;
    },
    p(e, o) {
      l && l.p && (!r || o & /*$$scope*/
      64) && ge(
        l,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? de(
          s,
          /*$$scope*/
          e[6],
          o,
          null
        ) : ue(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (b(l, e), r = !0);
    },
    o(e) {
      I(l, e), r = !1;
    },
    d(e) {
      e && v(t), l && l.d(e), n[9](null);
    }
  };
}
function he(n) {
  let t, r, s, l, e = (
    /*$$slots*/
    n[4].default && j(n)
  );
  return {
    c() {
      t = G("react-portal-target"), r = me(), e && e.c(), s = ce(), M(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      w(o, t, i), n[8](t), w(o, r, i), e && e.m(o, i), w(o, s, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = j(o), e.c(), b(e, 1), e.m(s.parentNode, s)) : e && (fe(), I(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(o) {
      l || (b(e), l = !0);
    },
    o(o) {
      I(e), l = !1;
    },
    d(o) {
      o && (v(t), v(r), v(s)), n[8](null), e && e.d(o);
    }
  };
}
function P(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function ye(n, t, r) {
  let s, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const i = ie(e);
  let {
    svelteInit: d
  } = t;
  const f = g(P(t)), a = g();
  k(n, a, (c) => r(0, s = c));
  const u = g();
  k(n, u, (c) => r(1, l = c));
  const p = [], W = we("$$ms-gr-antd-react-wrapper"), {
    slotKey: z,
    slotIndex: U,
    subSlotIndex: H
  } = Q() || {}, K = d({
    parent: W,
    props: f,
    target: a,
    slot: u,
    slotKey: z,
    slotIndex: U,
    subSlotIndex: H,
    onDestroy(c) {
      p.push(c);
    }
  });
  xe("$$ms-gr-antd-react-wrapper", K), ve(() => {
    f.set(P(t));
  }), be(() => {
    p.forEach((c) => c());
  });
  function q(c) {
    R[c ? "unshift" : "push"](() => {
      s = c, a.set(s);
    });
  }
  function B(c) {
    R[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  return n.$$set = (c) => {
    r(17, t = C(C({}, t), O(c))), "svelteInit" in c && r(5, d = c.svelteInit), "$$scope" in c && r(6, o = c.$$scope);
  }, t = O(t), [s, l, a, u, i, d, o, e, q, B];
}
class Ie extends se {
  constructor(t) {
    super(), pe(this, t, ye, he, _e, {
      svelteInit: 5
    });
  }
}
const L = window.ms_globals.rerender, h = window.ms_globals.tree;
function Se(n) {
  function t(r) {
    const s = g(), l = new Ie({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? h;
          return i.nodes = [...i.nodes, o], L({
            createPortal: E,
            node: h
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== s), L({
              createPortal: E,
              node: h
            });
          }), o;
        },
        ...r.props
      }
    });
    return s.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
function Ee(n) {
  const [t, r] = J(() => m(n));
  return N(() => {
    let s = !0;
    return n.subscribe((e) => {
      s && (s = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function Ce(n) {
  const t = A(() => X(n, (r) => r), [n]);
  return Ee(t);
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !Re.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function T(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((s) => {
    n.getEventListeners(s).forEach(({
      listener: e,
      type: o,
      useCapture: i
    }) => {
      t.addEventListener(o, e, i);
    });
  });
  const r = Array.from(n.children);
  for (let s = 0; s < r.length; s++) {
    const l = r[s], e = T(l);
    t.replaceChild(e, t.children[s]);
  }
  return t;
}
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const y = V(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, l) => {
  const e = Y();
  return N(() => {
    var f;
    if (!e.current || !n)
      return;
    let o = n;
    function i() {
      let a = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (a = o.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(l, a), r && a.classList.add(...r.split(" ")), s) {
        const u = ke(s);
        Object.keys(u).forEach((p) => {
          a.style[p] = u[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var u;
        o = T(n), o.style.display = "contents", i(), (u = e.current) == null || u.appendChild(o);
      };
      a(), d = new window.MutationObserver(() => {
        var u, p;
        (u = e.current) != null && u.contains(o) && ((p = e.current) == null || p.removeChild(o)), a();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (f = e.current) == null || f.appendChild(o);
    return () => {
      var a, u;
      o.style.display = "", (a = e.current) != null && a.contains(o) && ((u = e.current) == null || u.removeChild(o)), d == null || d.disconnect();
    };
  }, [n, t, r, s, l]), S.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function je(n, t) {
  const r = A(() => S.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, o) => {
    if (e.props.node.slotIndex && o.props.node.slotIndex) {
      const i = m(e.props.node.slotIndex) || 0, d = m(o.props.node.slotIndex) || 0;
      return i - d === 0 && e.props.node.subSlotIndex && o.props.node.subSlotIndex ? (m(e.props.node.subSlotIndex) || 0) - (m(o.props.node.subSlotIndex) || 0) : i - d;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Ce(r);
}
const Le = Se(({
  slots: n,
  children: t,
  ...r
}) => {
  var l, e, o, i, d, f;
  const s = je(t);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ _.jsx(Z.Group, {
      ...r,
      max: {
        ...r.max,
        popover: n["max.popover.title"] || n["max.popover.content"] ? {
          ...((e = r.max) == null ? void 0 : e.popover) || {},
          title: n["max.popover.title"] ? /* @__PURE__ */ _.jsx(y, {
            slot: n["max.popover.title"]
          }) : (i = (o = r.max) == null ? void 0 : o.popover) == null ? void 0 : i.title,
          content: n["max.popover.content"] ? /* @__PURE__ */ _.jsx(y, {
            slot: n["max.popover.content"]
          }) : (f = (d = r.max) == null ? void 0 : d.popover) == null ? void 0 : f.content
        } : (l = r.max) == null ? void 0 : l.popover
      },
      children: s.map((a, u) => /* @__PURE__ */ _.jsx(y, {
        slot: a
      }, u))
    })]
  });
});
export {
  Le as AvatarGroup,
  Le as default
};
