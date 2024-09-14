import { g as X, w as p } from "./Index-DX4E8Hze.js";
const F = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, V = window.ms_globals.React.useEffect, L = window.ms_globals.React.useMemo, C = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Tabs;
var N = {
  exports: {}
}, v = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var K = F, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = K.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(e, t, o) {
  var l, s = {}, n = null, r = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (l in t) te.call(t, l) && !re.hasOwnProperty(l) && (s[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) s[l] === void 0 && (s[l] = t[l]);
  return {
    $$typeof: $,
    type: e,
    key: n,
    ref: r,
    props: s,
    _owner: ne.current
  };
}
v.Fragment = ee;
v.jsx = z;
v.jsxs = z;
N.exports = v;
var b = N.exports;
const {
  SvelteComponent: oe,
  assign: I,
  binding_callbacks: j,
  check_outros: le,
  component_subscribe: O,
  compute_slots: se,
  create_slot: ce,
  detach: m,
  element: T,
  empty: ie,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ae,
  get_slot_changes: ue,
  group_outros: de,
  init: fe,
  insert: h,
  safe_not_equal: _e,
  set_custom_element_data: D,
  space: be,
  transition_in: w,
  transition_out: y,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: me,
  onDestroy: he,
  setContext: we
} = window.__gradio__svelte__internal;
function S(e) {
  let t, o;
  const l = (
    /*#slots*/
    e[7].default
  ), s = ce(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = T("svelte-slot"), s && s.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      h(n, t, r), s && s.m(t, null), e[9](t), o = !0;
    },
    p(n, r) {
      s && s.p && (!o || r & /*$$scope*/
      64) && ge(
        s,
        l,
        n,
        /*$$scope*/
        n[6],
        o ? ue(
          l,
          /*$$scope*/
          n[6],
          r,
          null
        ) : ae(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (w(s, n), o = !0);
    },
    o(n) {
      y(s, n), o = !1;
    },
    d(n) {
      n && m(t), s && s.d(n), e[9](null);
    }
  };
}
function ve(e) {
  let t, o, l, s, n = (
    /*$$slots*/
    e[4].default && S(e)
  );
  return {
    c() {
      t = T("react-portal-target"), o = be(), n && n.c(), l = ie(), D(t, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      h(r, t, c), e[8](t), h(r, o, c), n && n.m(r, c), h(r, l, c), s = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, c), c & /*$$slots*/
      16 && w(n, 1)) : (n = S(r), n.c(), w(n, 1), n.m(l.parentNode, l)) : n && (de(), y(n, 1, 1, () => {
        n = null;
      }), le());
    },
    i(r) {
      s || (w(n), s = !0);
    },
    o(r) {
      y(n), s = !1;
    },
    d(r) {
      r && (m(t), m(o), m(l)), e[8](null), n && n.d(r);
    }
  };
}
function k(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function xe(e, t, o) {
  let l, s, {
    $$slots: n = {},
    $$scope: r
  } = t;
  const c = se(n);
  let {
    svelteInit: u
  } = t;
  const f = p(k(t)), i = p();
  O(e, i, (d) => o(0, l = d));
  const a = p();
  O(e, a, (d) => o(1, s = d));
  const _ = [], x = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: W,
    slotIndex: A,
    subSlotIndex: q
  } = X() || {}, G = u({
    parent: x,
    props: f,
    target: i,
    slot: a,
    slotKey: W,
    slotIndex: A,
    subSlotIndex: q,
    onDestroy(d) {
      _.push(d);
    }
  });
  we("$$ms-gr-antd-react-wrapper", G), pe(() => {
    f.set(k(t));
  }), he(() => {
    _.forEach((d) => d());
  });
  function H(d) {
    j[d ? "unshift" : "push"](() => {
      l = d, i.set(l);
    });
  }
  function J(d) {
    j[d ? "unshift" : "push"](() => {
      s = d, a.set(s);
    });
  }
  return e.$$set = (d) => {
    o(17, t = I(I({}, t), R(d))), "svelteInit" in d && o(5, u = d.svelteInit), "$$scope" in d && o(6, r = d.$$scope);
  }, t = R(t), [l, s, i, a, c, u, r, n, H, J];
}
class Ee extends oe {
  constructor(t) {
    super(), fe(this, t, xe, ve, _e, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, E = window.ms_globals.tree;
function ye(e) {
  function t(o) {
    const l = p(), s = new Ee({
      ...o,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? E;
          return c.nodes = [...c.nodes, r], P({
            createPortal: C,
            node: E
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== l), P({
              createPortal: C,
              node: E
            });
          }), r;
        },
        ...o.props
      }
    });
    return l.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const Ce = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const l = e[o];
    return typeof l == "number" && !Ce.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function M(e) {
  const t = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: n,
      type: r,
      useCapture: c
    }) => {
      t.addEventListener(r, n, c);
    });
  });
  const o = Array.from(e.children);
  for (let l = 0; l < o.length; l++) {
    const s = o[l], n = M(s);
    t.replaceChild(n, t.children[l]);
  }
  return t;
}
function je(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const g = Y(({
  slot: e,
  clone: t,
  className: o,
  style: l
}, s) => {
  const n = Q();
  return V(() => {
    var f;
    if (!n.current || !e)
      return;
    let r = e;
    function c() {
      let i = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (i = r.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), je(s, i), o && i.classList.add(...o.split(" ")), l) {
        const a = Ie(l);
        Object.keys(a).forEach((_) => {
          i.style[_] = a[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var a;
        r = M(e), r.style.display = "contents", c(), (a = n.current) == null || a.appendChild(r);
      };
      i(), u = new window.MutationObserver(() => {
        var a, _;
        (a = n.current) != null && a.contains(r) && ((_ = n.current) == null || _.removeChild(r)), i();
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", c(), (f = n.current) == null || f.appendChild(r);
    return () => {
      var i, a;
      r.style.display = "", (i = n.current) != null && i.contains(r) && ((a = n.current) == null || a.removeChild(r)), u == null || u.disconnect();
    };
  }, [e, t, o, l, s]), F.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  });
});
function Oe(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function B(e) {
  return L(() => Oe(e), [e]);
}
function Re(e) {
  return Object.keys(e).reduce((t, o) => (e[o] !== void 0 && (t[o] = e[o]), t), {});
}
function U(e, t) {
  return e.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const l = {
      ...o.props
    };
    let s = l;
    Object.keys(o.slots).forEach((r) => {
      if (!o.slots[r] || !(o.slots[r] instanceof Element) && !o.slots[r].el)
        return;
      const c = r.split(".");
      c.forEach((_, x) => {
        s[_] || (s[_] = {}), x !== c.length - 1 && (s = l[_]);
      });
      const u = o.slots[r];
      let f, i, a = !1;
      u instanceof Element ? f = u : (f = u.el, i = u.callback, a = u.clone || !1), s[c[c.length - 1]] = f ? i ? (..._) => (i(c[c.length - 1], _), /* @__PURE__ */ b.jsx(g, {
        slot: f,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ b.jsx(g, {
        slot: f,
        clone: a || (t == null ? void 0 : t.clone)
      }) : s[c[c.length - 1]], s = l;
    });
    const n = "children";
    return o[n] && (l[n] = U(o[n], t)), l;
  });
}
const ke = ye(({
  slots: e,
  indicator: t,
  items: o,
  onChange: l,
  onValueChange: s,
  slotItems: n,
  more: r,
  children: c,
  ...u
}) => {
  const f = B(t == null ? void 0 : t.size), i = B(r == null ? void 0 : r.getPopupContainer);
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [/* @__PURE__ */ b.jsx("div", {
      style: {
        display: "none"
      },
      children: c
    }), /* @__PURE__ */ b.jsx(Z, {
      ...u,
      indicator: f ? {
        ...t,
        size: f
      } : t,
      items: L(() => o || U(n), [o, n]),
      more: Re({
        ...r || {},
        getPopupContainer: i || (r == null ? void 0 : r.getPopupContainer),
        icon: e["more.icon"] ? /* @__PURE__ */ b.jsx(g, {
          slot: e["more.icon"]
        }) : r == null ? void 0 : r.icon
      }),
      tabBarExtraContent: e.tabBarExtraContent ? /* @__PURE__ */ b.jsx(g, {
        slot: e.tabBarExtraContent
      }) : e["tabBarExtraContent.left"] || e["tabBarExtraContent.right"] ? {
        left: e["tabBarExtraContent.left"] ? /* @__PURE__ */ b.jsx(g, {
          slot: e["tabBarExtraContent.left"]
        }) : void 0,
        right: e["tabBarExtraContent.right"] ? /* @__PURE__ */ b.jsx(g, {
          slot: e["tabBarExtraContent.right"]
        }) : void 0
      } : u.tabBarExtraContent,
      addIcon: e.addIcon ? /* @__PURE__ */ b.jsx(g, {
        slot: e.addIcon
      }) : u.addIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ b.jsx(g, {
        slot: e.removeIcon
      }) : u.removeIcon,
      onChange: (a) => {
        l == null || l(a), s(a);
      }
    })]
  });
});
export {
  ke as Tabs,
  ke as default
};
