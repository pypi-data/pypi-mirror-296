import { g as Y, w as m } from "./Index-SL179RD7.js";
const j = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, J = window.ms_globals.React.useMemo, C = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.Tooltip;
var F = {
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
var V = j, X = Symbol.for("react.element"), Z = Symbol.for("react.fragment"), $ = Object.prototype.hasOwnProperty, ee = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, te = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function L(n, t, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (r in t) $.call(t, r) && !te.hasOwnProperty(r) && (l[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: X,
    type: n,
    key: e,
    ref: o,
    props: l,
    _owner: ee.current
  };
}
h.Fragment = Z;
h.jsx = L;
h.jsxs = L;
F.exports = h;
var p = F.exports;
const {
  SvelteComponent: ne,
  assign: x,
  binding_callbacks: E,
  check_outros: oe,
  component_subscribe: I,
  compute_slots: re,
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
  set_custom_element_data: T,
  space: fe,
  transition_in: b,
  transition_out: v,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: me,
  onDestroy: ge,
  setContext: we
} = window.__gradio__svelte__internal;
function O(n) {
  let t, s;
  const r = (
    /*#slots*/
    n[7].default
  ), l = se(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = N("svelte-slot"), l && l.c(), T(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      w(e, t, o), l && l.m(t, null), n[9](t), s = !0;
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
      s || (b(l, e), s = !0);
    },
    o(e) {
      v(l, e), s = !1;
    },
    d(e) {
      e && g(t), l && l.d(e), n[9](null);
    }
  };
}
function be(n) {
  let t, s, r, l, e = (
    /*$$slots*/
    n[4].default && O(n)
  );
  return {
    c() {
      t = N("react-portal-target"), s = fe(), e && e.c(), r = le(), T(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      w(o, t, i), n[8](t), w(o, s, i), e && e.m(o, i), w(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = O(o), e.c(), b(e, 1), e.m(r.parentNode, r)) : e && (ae(), v(e, 1, 1, () => {
        e = null;
      }), oe());
    },
    i(o) {
      l || (b(e), l = !0);
    },
    o(o) {
      v(e), l = !1;
    },
    d(o) {
      o && (g(t), g(s), g(r)), n[8](null), e && e.d(o);
    }
  };
}
function S(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function he(n, t, s) {
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const i = re(e);
  let {
    svelteInit: d
  } = t;
  const _ = m(S(t)), c = m();
  I(n, c, (a) => s(0, r = a));
  const u = m();
  I(n, u, (a) => s(1, l = a));
  const f = [], M = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: W,
    slotIndex: z,
    subSlotIndex: A
  } = Y() || {}, U = d({
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
  we("$$ms-gr-antd-react-wrapper", U), pe(() => {
    _.set(S(t));
  }), ge(() => {
    f.forEach((a) => a());
  });
  function q(a) {
    E[a ? "unshift" : "push"](() => {
      r = a, c.set(r);
    });
  }
  function G(a) {
    E[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return n.$$set = (a) => {
    s(17, t = x(x({}, t), R(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, o = a.$$scope);
  }, t = R(t), [r, l, c, u, i, d, o, e, q, G];
}
class ye extends ne {
  constructor(t) {
    super(), ue(this, t, he, be, de, {
      svelteInit: 5
    });
  }
}
const k = window.ms_globals.rerender, y = window.ms_globals.tree;
function ve(n) {
  function t(s) {
    const r = m(), l = new ye({
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
          }, i = e.parent ?? y;
          return i.nodes = [...i.nodes, o], k({
            createPortal: C,
            node: y
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), k({
              createPortal: C,
              node: y
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
const Ce = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const r = n[s];
    return typeof r == "number" && !Ce.includes(s) ? t[s] = r + "px" : t[s] = r, t;
  }, {}) : {};
}
function D(n) {
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
    const l = s[r], e = D(l);
    t.replaceChild(e, t.children[r]);
  }
  return t;
}
function Ee(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Ie = H(({
  slot: n,
  clone: t,
  className: s,
  style: r
}, l) => {
  const e = K();
  return B(() => {
    var _;
    if (!e.current || !n)
      return;
    let o = n;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ee(l, c), s && c.classList.add(...s.split(" ")), r) {
        const u = xe(r);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var u;
        o = D(n), o.style.display = "contents", i(), (u = e.current) == null || u.appendChild(o);
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
  }, [n, t, s, r, l]), j.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Re(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function P(n) {
  return J(() => Re(n), [n]);
}
const Se = ve(({
  slots: n,
  afterOpenChange: t,
  getPopupContainer: s,
  children: r,
  ...l
}) => {
  const e = P(t), o = P(s);
  return /* @__PURE__ */ p.jsx(p.Fragment, {
    children: /* @__PURE__ */ p.jsx(Q, {
      ...l,
      afterOpenChange: e,
      getPopupContainer: o,
      title: n.title ? /* @__PURE__ */ p.jsx(Ie, {
        slot: n.title
      }) : l.title,
      children: r
    })
  });
});
export {
  Se as Tooltip,
  Se as default
};
