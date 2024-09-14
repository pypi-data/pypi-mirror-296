import { g as Q, w as m } from "./Index-2dEGuET6.js";
const L = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, K = window.ms_globals.React.useEffect, F = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Tour;
var N = {
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
var Z = L, V = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function T(n, t, o) {
  var s, l = {}, e = null, r = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (s in t) ee.call(t, s) && !ne.hasOwnProperty(s) && (l[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) l[s] === void 0 && (l[s] = t[s]);
  return {
    $$typeof: V,
    type: n,
    key: e,
    ref: r,
    props: l,
    _owner: te.current
  };
}
h.Fragment = $;
h.jsx = T;
h.jsxs = T;
N.exports = h;
var p = N.exports;
const {
  SvelteComponent: re,
  assign: k,
  binding_callbacks: O,
  check_outros: oe,
  component_subscribe: R,
  compute_slots: se,
  create_slot: le,
  detach: g,
  element: D,
  empty: ce,
  exclude_internal_props: S,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ae,
  group_outros: ue,
  init: de,
  insert: b,
  safe_not_equal: fe,
  set_custom_element_data: M,
  space: _e,
  transition_in: w,
  transition_out: E,
  update_slot_base: pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: me,
  getContext: ge,
  onDestroy: be,
  setContext: we
} = window.__gradio__svelte__internal;
function C(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), l = le(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), l && l.c(), M(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      b(e, t, r), l && l.m(t, null), n[9](t), o = !0;
    },
    p(e, r) {
      l && l.p && (!o || r & /*$$scope*/
      64) && pe(
        l,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? ae(
          s,
          /*$$scope*/
          e[6],
          r,
          null
        ) : ie(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (w(l, e), o = !0);
    },
    o(e) {
      E(l, e), o = !1;
    },
    d(e) {
      e && g(t), l && l.d(e), n[9](null);
    }
  };
}
function he(n) {
  let t, o, s, l, e = (
    /*$$slots*/
    n[4].default && C(n)
  );
  return {
    c() {
      t = D("react-portal-target"), o = _e(), e && e.c(), s = ce(), M(t, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      b(r, t, c), n[8](t), b(r, o, c), e && e.m(r, c), b(r, s, c), l = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, c), c & /*$$slots*/
      16 && w(e, 1)) : (e = C(r), e.c(), w(e, 1), e.m(s.parentNode, s)) : e && (ue(), E(e, 1, 1, () => {
        e = null;
      }), oe());
    },
    i(r) {
      l || (w(e), l = !0);
    },
    o(r) {
      E(e), l = !1;
    },
    d(r) {
      r && (g(t), g(o), g(s)), n[8](null), e && e.d(r);
    }
  };
}
function j(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function ye(n, t, o) {
  let s, l, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const c = se(e);
  let {
    svelteInit: u
  } = t;
  const _ = m(j(t)), i = m();
  R(n, i, (d) => o(0, s = d));
  const a = m();
  R(n, a, (d) => o(1, l = d));
  const f = [], y = ge("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: U,
    subSlotIndex: q
  } = Q() || {}, G = u({
    parent: y,
    props: _,
    target: i,
    slot: a,
    slotKey: A,
    slotIndex: U,
    subSlotIndex: q,
    onDestroy(d) {
      f.push(d);
    }
  });
  we("$$ms-gr-antd-react-wrapper", G), me(() => {
    _.set(j(t));
  }), be(() => {
    f.forEach((d) => d());
  });
  function H(d) {
    O[d ? "unshift" : "push"](() => {
      s = d, i.set(s);
    });
  }
  function B(d) {
    O[d ? "unshift" : "push"](() => {
      l = d, a.set(l);
    });
  }
  return n.$$set = (d) => {
    o(17, t = k(k({}, t), S(d))), "svelteInit" in d && o(5, u = d.svelteInit), "$$scope" in d && o(6, r = d.$$scope);
  }, t = S(t), [s, l, i, a, c, u, r, e, H, B];
}
class ve extends re {
  constructor(t) {
    super(), de(this, t, ye, he, fe, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, v = window.ms_globals.tree;
function Ee(n) {
  function t(o) {
    const s = m(), l = new ve({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
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
          }, c = e.parent ?? v;
          return c.nodes = [...c.nodes, r], P({
            createPortal: I,
            node: v
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== s), P({
              createPortal: I,
              node: v
            });
          }), r;
        },
        ...o.props
      }
    });
    return s.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !xe.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function W(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((s) => {
    n.getEventListeners(s).forEach(({
      listener: e,
      type: r,
      useCapture: c
    }) => {
      t.addEventListener(r, e, c);
    });
  });
  const o = Array.from(n.children);
  for (let s = 0; s < o.length; s++) {
    const l = o[s], e = W(l);
    t.replaceChild(e, t.children[s]);
  }
  return t;
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const x = J(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, l) => {
  const e = Y();
  return K(() => {
    var _;
    if (!e.current || !n)
      return;
    let r = n;
    function c() {
      let i = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (i = r.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), ke(l, i), o && i.classList.add(...o.split(" ")), s) {
        const a = Ie(s);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var a;
        r = W(n), r.style.display = "contents", c(), (a = e.current) == null || a.appendChild(r);
      };
      i(), u = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(r) && ((f = e.current) == null || f.removeChild(r)), i();
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", c(), (_ = e.current) == null || _.appendChild(r);
    return () => {
      var i, a;
      r.style.display = "", (i = e.current) != null && i.contains(r) && ((a = e.current) == null || a.removeChild(r)), u == null || u.disconnect();
    };
  }, [n, t, o, s, l]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Oe(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Re(n) {
  return F(() => Oe(n), [n]);
}
function z(n, t) {
  return n.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const s = {
      ...o.props
    };
    let l = s;
    Object.keys(o.slots).forEach((r) => {
      if (!o.slots[r] || !(o.slots[r] instanceof Element) && !o.slots[r].el)
        return;
      const c = r.split(".");
      c.forEach((f, y) => {
        l[f] || (l[f] = {}), y !== c.length - 1 && (l = s[f]);
      });
      const u = o.slots[r];
      let _, i, a = !1;
      u instanceof Element ? _ = u : (_ = u.el, i = u.callback, a = u.clone || !1), l[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ p.jsx(x, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ p.jsx(x, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      }) : l[c[c.length - 1]], l = s;
    });
    const e = "children";
    return o[e] && (s[e] = z(o[e], t)), s;
  });
}
const Ce = Ee(({
  slots: n,
  steps: t,
  slotItems: o,
  children: s,
  onChange: l,
  onClose: e,
  onValueChange: r,
  getPopupContainer: c,
  ...u
}) => {
  const _ = Re(c);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: s
    }), /* @__PURE__ */ p.jsx(X, {
      ...u,
      steps: F(() => t || z(o), [t, o]),
      onChange: (i) => {
        l == null || l(i), r({
          open: !0,
          current: i
        });
      },
      closeIcon: n.closeIcon ? /* @__PURE__ */ p.jsx(x, {
        slot: n.closeIcon
      }) : u.closeIcon,
      getPopupContainer: _,
      onClose: (i, ...a) => {
        e == null || e(i, ...a), r({
          current: i,
          open: !1
        });
      }
    })]
  });
});
export {
  Ce as Tour,
  Ce as default
};
