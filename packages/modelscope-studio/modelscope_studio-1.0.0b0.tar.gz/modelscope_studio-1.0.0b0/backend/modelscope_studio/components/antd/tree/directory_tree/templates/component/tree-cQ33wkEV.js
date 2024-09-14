import { g as Z, w as v } from "./Index-kbzhHBia.js";
const W = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useEffect, z = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, K = window.ms_globals.antd.Tree;
var A = {
  exports: {}
}, j = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var V = W, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(e, n, o) {
  var r, l = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (r in n) te.call(n, r) && !re.hasOwnProperty(r) && (l[r] = n[r]);
  if (e && e.defaultProps) for (r in n = e.defaultProps, n) l[r] === void 0 && (l[r] = n[r]);
  return {
    $$typeof: $,
    type: e,
    key: t,
    ref: s,
    props: l,
    _owner: ne.current
  };
}
j.Fragment = ee;
j.jsx = q;
j.jsxs = q;
A.exports = j;
var g = A.exports;
const {
  SvelteComponent: oe,
  assign: P,
  binding_callbacks: D,
  check_outros: se,
  component_subscribe: F,
  compute_slots: le,
  create_slot: ce,
  detach: I,
  element: G,
  empty: ie,
  exclude_internal_props: N,
  get_all_dirty_from_scope: ae,
  get_slot_changes: de,
  group_outros: ue,
  init: fe,
  insert: x,
  safe_not_equal: _e,
  set_custom_element_data: H,
  space: ge,
  transition_in: E,
  transition_out: C,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: he,
  getContext: me,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function T(e) {
  let n, o;
  const r = (
    /*#slots*/
    e[7].default
  ), l = ce(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = G("svelte-slot"), l && l.c(), H(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      x(t, n, s), l && l.m(n, null), e[9](n), o = !0;
    },
    p(t, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && we(
        l,
        r,
        t,
        /*$$scope*/
        t[6],
        o ? de(
          r,
          /*$$scope*/
          t[6],
          s,
          null
        ) : ae(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (E(l, t), o = !0);
    },
    o(t) {
      C(l, t), o = !1;
    },
    d(t) {
      t && I(n), l && l.d(t), e[9](null);
    }
  };
}
function pe(e) {
  let n, o, r, l, t = (
    /*$$slots*/
    e[4].default && T(e)
  );
  return {
    c() {
      n = G("react-portal-target"), o = ge(), t && t.c(), r = ie(), H(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      x(s, n, c), e[8](n), x(s, o, c), t && t.m(s, c), x(s, r, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && E(t, 1)) : (t = T(s), t.c(), E(t, 1), t.m(r.parentNode, r)) : t && (ue(), C(t, 1, 1, () => {
        t = null;
      }), se());
    },
    i(s) {
      l || (E(t), l = !0);
    },
    o(s) {
      C(t), l = !1;
    },
    d(s) {
      s && (I(n), I(o), I(r)), e[8](null), t && t.d(s);
    }
  };
}
function M(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function ve(e, n, o) {
  let r, l, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const c = le(t);
  let {
    svelteInit: f
  } = n;
  const _ = v(M(n)), a = v();
  F(e, a, (d) => o(0, r = d));
  const u = v();
  F(e, u, (d) => o(1, l = d));
  const i = [], m = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: y,
    slotIndex: b,
    subSlotIndex: O
  } = Z() || {}, k = f({
    parent: m,
    props: _,
    target: a,
    slot: u,
    slotKey: y,
    slotIndex: b,
    subSlotIndex: O,
    onDestroy(d) {
      i.push(d);
    }
  });
  ye("$$ms-gr-antd-react-wrapper", k), he(() => {
    _.set(M(n));
  }), be(() => {
    i.forEach((d) => d());
  });
  function L(d) {
    D[d ? "unshift" : "push"](() => {
      r = d, a.set(r);
    });
  }
  function w(d) {
    D[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  return e.$$set = (d) => {
    o(17, n = P(P({}, n), N(d))), "svelteInit" in d && o(5, f = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, n = N(n), [r, l, a, u, c, f, s, t, L, w];
}
class Ie extends oe {
  constructor(n) {
    super(), fe(this, n, ve, pe, _e, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, R = window.ms_globals.tree;
function xe(e) {
  function n(o) {
    const r = v(), l = new Ie({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? R;
          return c.nodes = [...c.nodes, s], U({
            createPortal: S,
            node: R
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((f) => f.svelteInstance !== r), U({
              createPortal: S,
              node: R
            });
          }), s;
        },
        ...o.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Ee = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const r = e[o];
    return typeof r == "number" && !Ee.includes(o) ? n[o] = r + "px" : n[o] = r, n;
  }, {}) : {};
}
function B(e) {
  const n = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: t,
      type: s,
      useCapture: c
    }) => {
      n.addEventListener(s, t, c);
    });
  });
  const o = Array.from(e.children);
  for (let r = 0; r < o.length; r++) {
    const l = o[r], t = B(l);
    n.replaceChild(t, n.children[r]);
  }
  return n;
}
function Oe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const h = Y(({
  slot: e,
  clone: n,
  className: o,
  style: r
}, l) => {
  const t = Q();
  return X(() => {
    var _;
    if (!t.current || !e)
      return;
    let s = e;
    function c() {
      let a = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (a = s.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(l, a), o && a.classList.add(...o.split(" ")), r) {
        const u = je(r);
        Object.keys(u).forEach((i) => {
          a.style[i] = u[i];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var u;
        s = B(e), s.style.display = "contents", c(), (u = t.current) == null || u.appendChild(s);
      };
      a(), f = new window.MutationObserver(() => {
        var u, i;
        (u = t.current) != null && u.contains(s) && ((i = t.current) == null || i.removeChild(s)), a();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      s.style.display = "contents", c(), (_ = t.current) == null || _.appendChild(s);
    return () => {
      var a, u;
      s.style.display = "", (a = t.current) != null && a.contains(s) && ((u = t.current) == null || u.removeChild(s)), f == null || f.disconnect();
    };
  }, [e, n, o, r, l]), W.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function ke(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function p(e) {
  return z(() => ke(e), [e]);
}
function Le(e) {
  return Object.keys(e).reduce((n, o) => (e[o] !== void 0 && (n[o] = e[o]), n), {});
}
function J(e, n) {
  return e.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const r = {
      ...o.props
    };
    let l = r;
    Object.keys(o.slots).forEach((s) => {
      if (!o.slots[s] || !(o.slots[s] instanceof Element) && !o.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((i, m) => {
        l[i] || (l[i] = {}), m !== c.length - 1 && (l = r[i]);
      });
      const f = o.slots[s];
      let _, a, u = !1;
      f instanceof Element ? _ = f : (_ = f.el, a = f.callback, u = f.clone || !1), l[c[c.length - 1]] = _ ? a ? (...i) => (a(c[c.length - 1], i), /* @__PURE__ */ g.jsx(h, {
        slot: _,
        clone: u || (n == null ? void 0 : n.clone)
      })) : /* @__PURE__ */ g.jsx(h, {
        slot: _,
        clone: u || (n == null ? void 0 : n.clone)
      }) : l[c[c.length - 1]], l = r;
    });
    const t = "children";
    return o[t] && (r[t] = J(o[t], n)), r;
  });
}
const Ce = xe(({
  slots: e,
  filterTreeNode: n,
  treeData: o,
  draggable: r,
  allowDrop: l,
  onValueChange: t,
  onCheck: s,
  onSelect: c,
  onExpand: f,
  children: _,
  directory: a,
  slotItems: u,
  ...i
}) => {
  const m = p(n), y = p(r), b = p(typeof r == "object" ? r.nodeDraggable : void 0), O = p(l), k = a ? K.DirectoryTree : K, L = z(() => ({
    ...i,
    treeData: o || J(u),
    showLine: e["showLine.showLeafIcon"] ? {
      showLeafIcon: /* @__PURE__ */ g.jsx(h, {
        slot: e["showLine.showLeafIcon"]
      })
    } : i.showLine,
    icon: e.icon ? /* @__PURE__ */ g.jsx(h, {
      slot: e.icon
    }) : i.icon,
    switcherLoadingIcon: e.switcherLoadingIcon ? /* @__PURE__ */ g.jsx(h, {
      slot: e.switcherLoadingIcon
    }) : i.switcherLoadingIcon,
    switcherIcon: e.switcherIcon ? /* @__PURE__ */ g.jsx(h, {
      slot: e.switcherIcon
    }) : i.switcherIcon,
    draggable: e["draggable.icon"] || b ? {
      icon: e["draggable.icon"] ? /* @__PURE__ */ g.jsx(h, {
        slot: e["draggable.icon"]
      }) : typeof r == "object" ? r.icon : void 0,
      nodeDraggable: b
    } : y || r
  }), [r, y, b, i, u, e, o]);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: _
    }), /* @__PURE__ */ g.jsx(k, {
      ...Le(L),
      filterTreeNode: m,
      allowDrop: O,
      onSelect: (w, ...d) => {
        c == null || c(w, ...d), t({
          selectedKeys: w,
          expandedKeys: i.expandedKeys,
          checkedKeys: i.checkedKeys
        });
      },
      onExpand: (w, ...d) => {
        f == null || f(w, ...d), t({
          expandedKeys: w,
          selectedKeys: i.selectedKeys,
          checkedKeys: i.checkedKeys
        });
      },
      onCheck: (w, ...d) => {
        s == null || s(w, ...d), t({
          checkedKeys: w,
          selectedKeys: i.selectedKeys,
          expandedKeys: i.expandedKeys
        });
      }
    })]
  });
});
export {
  Ce as Tree,
  Ce as default
};
