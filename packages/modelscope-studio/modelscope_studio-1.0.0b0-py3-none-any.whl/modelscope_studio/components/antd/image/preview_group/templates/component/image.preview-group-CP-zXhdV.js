import { g as Y, w as p } from "./Index-y7PnHk0Q.js";
const j = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, J = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.Image;
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
var V = j, X = Symbol.for("react.element"), Z = Symbol.for("react.fragment"), $ = Object.prototype.hasOwnProperty, ee = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, te = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(t, n, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (r in n) $.call(n, r) && !te.hasOwnProperty(r) && (l[r] = n[r]);
  if (t && t.defaultProps) for (r in n = t.defaultProps, n) l[r] === void 0 && (l[r] = n[r]);
  return {
    $$typeof: X,
    type: t,
    key: e,
    ref: o,
    props: l,
    _owner: ee.current
  };
}
b.Fragment = Z;
b.jsx = F;
b.jsxs = F;
L.exports = b;
var v = L.exports;
const {
  SvelteComponent: ne,
  assign: C,
  binding_callbacks: k,
  check_outros: re,
  component_subscribe: x,
  compute_slots: oe,
  create_slot: se,
  detach: m,
  element: N,
  empty: le,
  exclude_internal_props: E,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ce,
  group_outros: ae,
  init: ue,
  insert: g,
  safe_not_equal: de,
  set_custom_element_data: D,
  space: fe,
  transition_in: w,
  transition_out: y,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: me,
  onDestroy: ge,
  setContext: we
} = window.__gradio__svelte__internal;
function R(t) {
  let n, s;
  const r = (
    /*#slots*/
    t[7].default
  ), l = se(
    r,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = N("svelte-slot"), l && l.c(), D(n, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      g(e, n, o), l && l.m(n, null), t[9](n), s = !0;
    },
    p(e, o) {
      l && l.p && (!s || o & /*$$scope*/
      64) && _e(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? ce(
          r,
          /*$$scope*/
          e[6],
          o,
          null
        ) : ie(
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
      e && m(n), l && l.d(e), t[9](null);
    }
  };
}
function be(t) {
  let n, s, r, l, e = (
    /*$$slots*/
    t[4].default && R(t)
  );
  return {
    c() {
      n = N("react-portal-target"), s = fe(), e && e.c(), r = le(), D(n, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      g(o, n, i), t[8](n), g(o, s, i), e && e.m(o, i), g(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && w(e, 1)) : (e = R(o), e.c(), w(e, 1), e.m(r.parentNode, r)) : e && (ae(), y(e, 1, 1, () => {
        e = null;
      }), re());
    },
    i(o) {
      l || (w(e), l = !0);
    },
    o(o) {
      y(e), l = !1;
    },
    d(o) {
      o && (m(n), m(s), m(r)), t[8](null), e && e.d(o);
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
  const i = oe(e);
  let {
    svelteInit: d
  } = n;
  const _ = p(S(n)), c = p();
  x(t, c, (a) => s(0, r = a));
  const u = p();
  x(t, u, (a) => s(1, l = a));
  const f = [], M = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: W,
    slotIndex: z,
    subSlotIndex: A
  } = Y() || {}, T = d({
    parent: M,
    props: _,
    target: c,
    slot: u,
    slotKey: W,
    slotIndex: z,
    subSlotIndex: A,
    onDestroy(a) {
      f.push(a);
    }
  });
  we("$$ms-gr-antd-react-wrapper", T), pe(() => {
    _.set(S(n));
  }), ge(() => {
    f.forEach((a) => a());
  });
  function U(a) {
    k[a ? "unshift" : "push"](() => {
      r = a, c.set(r);
    });
  }
  function q(a) {
    k[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return t.$$set = (a) => {
    s(17, n = C(C({}, n), E(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, o = a.$$scope);
  }, n = E(n), [r, l, c, u, i, d, o, e, U, q];
}
class he extends ne {
  constructor(n) {
    super(), ue(this, n, ve, be, de, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, h = window.ms_globals.tree;
function ye(t) {
  function n(s) {
    const r = p(), l = new he({
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
          }, i = e.parent ?? h;
          return i.nodes = [...i.nodes, o], O({
            createPortal: I,
            node: h
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), O({
              createPortal: I,
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
      s(n);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ce(t) {
  return t ? Object.keys(t).reduce((n, s) => {
    const r = t[s];
    return typeof r == "number" && !Ie.includes(s) ? n[s] = r + "px" : n[s] = r, n;
  }, {}) : {};
}
function G(t) {
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
    const l = s[r], e = G(l);
    n.replaceChild(e, n.children[r]);
  }
  return n;
}
function ke(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const P = H(({
  slot: t,
  clone: n,
  className: s,
  style: r
}, l) => {
  const e = K();
  return B(() => {
    var _;
    if (!e.current || !t)
      return;
    let o = t;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), ke(l, c), s && c.classList.add(...s.split(" ")), r) {
        const u = Ce(r);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var u;
        o = G(t), o.style.display = "contents", i(), (u = e.current) == null || u.appendChild(o);
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
  }, [t, n, s, r, l]), j.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function xe(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Ee(t) {
  return J(() => xe(t), [t]);
}
function Re(t) {
  return typeof t == "object" && t !== null ? t : {};
}
const Oe = ye(({
  slots: t,
  preview: n,
  ...s
}) => {
  const r = Re(n), l = t["preview.mask"] || t["preview.closeIcon"] || n !== !1, e = Ee(r.getContainer);
  return /* @__PURE__ */ v.jsx(Q.PreviewGroup, {
    ...s,
    preview: l ? {
      ...r,
      getContainer: e,
      ...t["preview.mask"] || Reflect.has(r, "mask") ? {
        mask: t["preview.mask"] ? /* @__PURE__ */ v.jsx(P, {
          slot: t["preview.mask"]
        }) : r.mask
      } : {},
      closeIcon: t["preview.closeIcon"] ? /* @__PURE__ */ v.jsx(P, {
        slot: t["preview.closeIcon"]
      }) : r.closeIcon
    } : !1
  });
});
export {
  Oe as ImagePreviewGroup,
  Oe as default
};
