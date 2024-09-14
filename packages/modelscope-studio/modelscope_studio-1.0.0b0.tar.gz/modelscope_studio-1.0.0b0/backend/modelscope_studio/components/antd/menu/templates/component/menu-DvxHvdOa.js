import { g as Q, w } from "./Index-C813-4SS.js";
const K = window.ms_globals.React, H = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useEffect, Y = window.ms_globals.React.useMemo, E = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Menu;
var M = {
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
var Z = K, V = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function N(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ee.call(t, l) && !re.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: V,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: te.current
  };
}
v.Fragment = $;
v.jsx = N;
v.jsxs = N;
M.exports = v;
var m = M.exports;
const {
  SvelteComponent: ne,
  assign: R,
  binding_callbacks: k,
  check_outros: se,
  component_subscribe: O,
  compute_slots: oe,
  create_slot: le,
  detach: b,
  element: C,
  empty: ce,
  exclude_internal_props: j,
  get_all_dirty_from_scope: ie,
  get_slot_changes: de,
  group_outros: ue,
  init: fe,
  insert: p,
  safe_not_equal: ae,
  set_custom_element_data: F,
  space: _e,
  transition_in: y,
  transition_out: I,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: pe,
  setContext: ye
} = window.__gradio__svelte__internal;
function S(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = le(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = C("svelte-slot"), o && o.c(), F(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      p(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && me(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? de(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ie(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (y(o, e), r = !0);
    },
    o(e) {
      I(o, e), r = !1;
    },
    d(e) {
      e && b(t), o && o.d(e), n[9](null);
    }
  };
}
function ge(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && S(n)
  );
  return {
    c() {
      t = C("react-portal-target"), r = _e(), e && e.c(), l = ce(), F(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      p(s, t, c), n[8](t), p(s, r, c), e && e.m(s, c), p(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && y(e, 1)) : (e = S(s), e.c(), y(e, 1), e.m(l.parentNode, l)) : e && (ue(), I(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(s) {
      o || (y(e), o = !0);
    },
    o(s) {
      I(e), o = !1;
    },
    d(s) {
      s && (b(t), b(r), b(l)), n[8](null), e && e.d(s);
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
function ve(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = oe(e);
  let {
    svelteInit: i
  } = t;
  const u = w(P(t)), d = w();
  O(n, d, (a) => r(0, l = a));
  const f = w();
  O(n, f, (a) => r(1, o = a));
  const _ = [], h = be("$$ms-gr-antd-react-wrapper"), {
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T
  } = Q() || {}, q = i({
    parent: h,
    props: u,
    target: d,
    slot: f,
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T,
    onDestroy(a) {
      _.push(a);
    }
  });
  ye("$$ms-gr-antd-react-wrapper", q), we(() => {
    u.set(P(t));
  }), pe(() => {
    _.forEach((a) => a());
  });
  function D(a) {
    k[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function G(a) {
    k[a ? "unshift" : "push"](() => {
      o = a, f.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = R(R({}, t), j(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = j(t), [l, o, d, f, c, i, s, e, D, G];
}
class he extends ne {
  constructor(t) {
    super(), fe(this, t, ve, ge, ae, {
      svelteInit: 5
    });
  }
}
const L = window.ms_globals.rerender, x = window.ms_globals.tree;
function xe(n) {
  function t(r) {
    const l = w(), o = new he({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, s], L({
            createPortal: E,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), L({
              createPortal: E,
              node: x
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ee(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Ie.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function U(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: e,
      type: s,
      useCapture: c
    }) => {
      t.addEventListener(s, e, c);
    });
  });
  const r = Array.from(n.children);
  for (let l = 0; l < r.length; l++) {
    const o = r[l], e = U(o);
    t.replaceChild(e, t.children[l]);
  }
  return t;
}
function Re(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const g = H(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = B();
  return J(() => {
    var u;
    if (!e.current || !n)
      return;
    let s = n;
    function c() {
      let d = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (d = s.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Re(o, d), r && d.classList.add(...r.split(" ")), l) {
        const f = Ee(l);
        Object.keys(f).forEach((_) => {
          d.style[_] = f[_];
        });
      }
    }
    let i = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var f;
        s = U(n), s.style.display = "contents", c(), (f = e.current) == null || f.appendChild(s);
      };
      d(), i = new window.MutationObserver(() => {
        var f, _;
        (f = e.current) != null && f.contains(s) && ((_ = e.current) == null || _.removeChild(s)), d();
      }), i.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      s.style.display = "contents", c(), (u = e.current) == null || u.appendChild(s);
    return () => {
      var d, f;
      s.style.display = "", (d = e.current) != null && d.contains(s) && ((f = e.current) == null || f.removeChild(s)), i == null || i.disconnect();
    };
  }, [n, t, r, l, o]), K.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function ke(n) {
  return Object.keys(n).reduce((t, r) => (n[r] !== void 0 && (t[r] = n[r]), t), {});
}
function W(n, t) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const l = {
      ...r.props
    };
    let o = l;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((_, h) => {
        o[_] || (o[_] = {}), h !== c.length - 1 && (o = l[_]);
      });
      const i = r.slots[s];
      let u, d, f = !1;
      i instanceof Element ? u = i : (u = i.el, d = i.callback, f = i.clone || !1), o[c[c.length - 1]] = u ? d ? (..._) => (d(c[c.length - 1], _), /* @__PURE__ */ m.jsx(g, {
        slot: u,
        clone: f || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ m.jsx(g, {
        slot: u,
        clone: f || (t == null ? void 0 : t.clone)
      }) : o[c[c.length - 1]], o = l;
    });
    const e = "children";
    return r[e] && (l[e] = W(r[e], t)), l;
  });
}
const je = xe(({
  slots: n,
  items: t,
  slotItems: r,
  children: l,
  onValueChange: o,
  onOpenChange: e,
  onSelect: s,
  onDeselect: c,
  ...i
}) => /* @__PURE__ */ m.jsxs(m.Fragment, {
  children: [l, /* @__PURE__ */ m.jsx(X, {
    ...ke(i),
    onOpenChange: (u) => {
      e == null || e(u), o == null || o({
        openKeys: u,
        selectedKeys: i.selectedKeys || []
      });
    },
    onSelect: (u) => {
      s == null || s(u), o == null || o({
        openKeys: i.openKeys || [],
        selectedKeys: u.selectedKeys
      });
    },
    onDeselect: (u) => {
      c == null || c(u), o == null || o({
        openKeys: i.openKeys || [],
        selectedKeys: u.selectedKeys
      });
    },
    items: Y(() => t || W(r), [t, r]),
    expandIcon: n.expandIcon ? /* @__PURE__ */ m.jsx(g, {
      slot: n.expandIcon,
      clone: !0
    }) : i.expandIcon,
    overflowedIndicator: n.overflowedIndicator ? /* @__PURE__ */ m.jsx(g, {
      slot: n.overflowedIndicator
    }) : i.overflowedIndicator
  })]
}));
export {
  je as Menu,
  je as default
};
