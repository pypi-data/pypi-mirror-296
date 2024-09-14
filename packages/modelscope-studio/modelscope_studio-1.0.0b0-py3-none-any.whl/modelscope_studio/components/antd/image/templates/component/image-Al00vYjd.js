import { g as Y, w as m } from "./Index-BCOyki4s.js";
const j = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, J = window.ms_globals.React.useMemo, C = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.Image;
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
function F(e, n, s) {
  var r, l = {}, t = null, o = null;
  s !== void 0 && (t = "" + s), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (r in n) $.call(n, r) && !te.hasOwnProperty(r) && (l[r] = n[r]);
  if (e && e.defaultProps) for (r in n = e.defaultProps, n) l[r] === void 0 && (l[r] = n[r]);
  return {
    $$typeof: X,
    type: e,
    key: t,
    ref: o,
    props: l,
    _owner: ee.current
  };
}
b.Fragment = Z;
b.jsx = F;
b.jsxs = F;
L.exports = b;
var p = L.exports;
const {
  SvelteComponent: ne,
  assign: k,
  binding_callbacks: x,
  check_outros: re,
  component_subscribe: E,
  compute_slots: oe,
  create_slot: se,
  detach: g,
  element: N,
  empty: le,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ce,
  group_outros: ae,
  init: ue,
  insert: w,
  safe_not_equal: de,
  set_custom_element_data: D,
  space: fe,
  transition_in: h,
  transition_out: I,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: me,
  onDestroy: ge,
  setContext: we
} = window.__gradio__svelte__internal;
function S(e) {
  let n, s;
  const r = (
    /*#slots*/
    e[7].default
  ), l = se(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = N("svelte-slot"), l && l.c(), D(n, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      w(t, n, o), l && l.m(n, null), e[9](n), s = !0;
    },
    p(t, o) {
      l && l.p && (!s || o & /*$$scope*/
      64) && _e(
        l,
        r,
        t,
        /*$$scope*/
        t[6],
        s ? ce(
          r,
          /*$$scope*/
          t[6],
          o,
          null
        ) : ie(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      s || (h(l, t), s = !0);
    },
    o(t) {
      I(l, t), s = !1;
    },
    d(t) {
      t && g(n), l && l.d(t), e[9](null);
    }
  };
}
function he(e) {
  let n, s, r, l, t = (
    /*$$slots*/
    e[4].default && S(e)
  );
  return {
    c() {
      n = N("react-portal-target"), s = fe(), t && t.c(), r = le(), D(n, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      w(o, n, i), e[8](n), w(o, s, i), t && t.m(o, i), w(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, i), i & /*$$slots*/
      16 && h(t, 1)) : (t = S(o), t.c(), h(t, 1), t.m(r.parentNode, r)) : t && (ae(), I(t, 1, 1, () => {
        t = null;
      }), re());
    },
    i(o) {
      l || (h(t), l = !0);
    },
    o(o) {
      I(t), l = !1;
    },
    d(o) {
      o && (g(n), g(s), g(r)), e[8](null), t && t.d(o);
    }
  };
}
function O(e) {
  const {
    svelteInit: n,
    ...s
  } = e;
  return s;
}
function be(e, n, s) {
  let r, l, {
    $$slots: t = {},
    $$scope: o
  } = n;
  const i = oe(t);
  let {
    svelteInit: d
  } = n;
  const _ = m(O(n)), c = m();
  E(e, c, (a) => s(0, r = a));
  const u = m();
  E(e, u, (a) => s(1, l = a));
  const f = [], W = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T
  } = Y() || {}, U = d({
    parent: W,
    props: _,
    target: c,
    slot: u,
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T,
    onDestroy(a) {
      f.push(a);
    }
  });
  we("$$ms-gr-antd-react-wrapper", U), pe(() => {
    _.set(O(n));
  }), ge(() => {
    f.forEach((a) => a());
  });
  function q(a) {
    x[a ? "unshift" : "push"](() => {
      r = a, c.set(r);
    });
  }
  function G(a) {
    x[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return e.$$set = (a) => {
    s(17, n = k(k({}, n), R(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, o = a.$$scope);
  }, n = R(n), [r, l, c, u, i, d, o, t, q, G];
}
class ve extends ne {
  constructor(n) {
    super(), ue(this, n, be, he, de, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, v = window.ms_globals.tree;
function ye(e) {
  function n(s) {
    const r = m(), l = new ve({
      ...s,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const o = {
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
          }, i = t.parent ?? v;
          return i.nodes = [...i.nodes, o], P({
            createPortal: C,
            node: v
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), P({
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
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ce(e) {
  return e ? Object.keys(e).reduce((n, s) => {
    const r = e[s];
    return typeof r == "number" && !Ie.includes(s) ? n[s] = r + "px" : n[s] = r, n;
  }, {}) : {};
}
function M(e) {
  const n = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: t,
      type: o,
      useCapture: i
    }) => {
      n.addEventListener(o, t, i);
    });
  });
  const s = Array.from(e.children);
  for (let r = 0; r < s.length; r++) {
    const l = s[r], t = M(l);
    n.replaceChild(t, n.children[r]);
  }
  return n;
}
function ke(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const y = H(({
  slot: e,
  clone: n,
  className: s,
  style: r
}, l) => {
  const t = K();
  return B(() => {
    var _;
    if (!t.current || !e)
      return;
    let o = e;
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
        o = M(e), o.style.display = "contents", i(), (u = t.current) == null || u.appendChild(o);
      };
      c(), d = new window.MutationObserver(() => {
        var u, f;
        (u = t.current) != null && u.contains(o) && ((f = t.current) == null || f.removeChild(o)), c();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (_ = t.current) == null || _.appendChild(o);
    return () => {
      var c, u;
      o.style.display = "", (c = t.current) != null && c.contains(o) && ((u = t.current) == null || u.removeChild(o)), d == null || d.disconnect();
    };
  }, [e, n, s, r, l]), j.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function xe(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Ee(e) {
  return J(() => xe(e), [e]);
}
function Re(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Oe = ye(({
  slots: e,
  preview: n,
  ...s
}) => {
  const r = Re(n), l = e["preview.mask"] || e["preview.closeIcon"] || n !== !1, t = Ee(r.getContainer);
  return /* @__PURE__ */ p.jsx(Q, {
    ...s,
    preview: l ? {
      ...r,
      getContainer: t,
      ...e["preview.mask"] || Reflect.has(r, "mask") ? {
        mask: e["preview.mask"] ? /* @__PURE__ */ p.jsx(y, {
          slot: e["preview.mask"]
        }) : r.mask
      } : {},
      closeIcon: e["preview.closeIcon"] ? /* @__PURE__ */ p.jsx(y, {
        slot: e["preview.closeIcon"]
      }) : r.closeIcon
    } : !1,
    placeholder: e.placeholder ? /* @__PURE__ */ p.jsx(y, {
      slot: e.placeholder
    }) : s.placeholder
  });
});
export {
  Oe as Image,
  Oe as default
};
