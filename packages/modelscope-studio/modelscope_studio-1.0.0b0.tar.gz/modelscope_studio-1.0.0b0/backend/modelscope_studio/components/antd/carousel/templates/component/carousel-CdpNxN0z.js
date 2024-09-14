import { g as Q, w as g, d as X, a as m } from "./Index-DKN5j0zL.js";
const I = window.ms_globals.React, C = window.ms_globals.React.useMemo, J = window.ms_globals.React.useState, N = window.ms_globals.React.useEffect, V = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, S = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Carousel;
var A = {
  exports: {}
}, y = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $ = I, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(t, n, s) {
  var o, l = {}, e = null, r = null;
  s !== void 0 && (e = "" + s), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (r = n.ref);
  for (o in n) ne.call(n, o) && !oe.hasOwnProperty(o) && (l[o] = n[o]);
  if (t && t.defaultProps) for (o in n = t.defaultProps, n) l[o] === void 0 && (l[o] = n[o]);
  return {
    $$typeof: ee,
    type: t,
    key: e,
    ref: r,
    props: l,
    _owner: re.current
  };
}
y.Fragment = te;
y.jsx = D;
y.jsxs = D;
A.exports = y;
var _ = A.exports;
const {
  SvelteComponent: se,
  assign: E,
  binding_callbacks: R,
  check_outros: le,
  component_subscribe: k,
  compute_slots: ie,
  create_slot: ae,
  detach: w,
  element: M,
  empty: ce,
  exclude_internal_props: O,
  get_all_dirty_from_scope: ue,
  get_slot_changes: de,
  group_outros: fe,
  init: pe,
  insert: b,
  safe_not_equal: _e,
  set_custom_element_data: T,
  space: me,
  transition_in: h,
  transition_out: x,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: he,
  setContext: ye
} = window.__gradio__svelte__internal;
function P(t) {
  let n, s;
  const o = (
    /*#slots*/
    t[7].default
  ), l = ae(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = M("svelte-slot"), l && l.c(), T(n, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      b(e, n, r), l && l.m(n, null), t[9](n), s = !0;
    },
    p(e, r) {
      l && l.p && (!s || r & /*$$scope*/
      64) && ge(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? de(
          o,
          /*$$scope*/
          e[6],
          r,
          null
        ) : ue(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (h(l, e), s = !0);
    },
    o(e) {
      x(l, e), s = !1;
    },
    d(e) {
      e && w(n), l && l.d(e), t[9](null);
    }
  };
}
function ve(t) {
  let n, s, o, l, e = (
    /*$$slots*/
    t[4].default && P(t)
  );
  return {
    c() {
      n = M("react-portal-target"), s = me(), e && e.c(), o = ce(), T(n, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      b(r, n, i), t[8](n), b(r, s, i), e && e.m(r, i), b(r, o, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = P(r), e.c(), h(e, 1), e.m(o.parentNode, o)) : e && (fe(), x(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(r) {
      l || (h(e), l = !0);
    },
    o(r) {
      x(e), l = !1;
    },
    d(r) {
      r && (w(n), w(s), w(o)), t[8](null), e && e.d(r);
    }
  };
}
function j(t) {
  const {
    svelteInit: n,
    ...s
  } = t;
  return s;
}
function xe(t, n, s) {
  let o, l, {
    $$slots: e = {},
    $$scope: r
  } = n;
  const i = ie(e);
  let {
    svelteInit: u
  } = n;
  const p = g(j(n)), a = g();
  k(t, a, (c) => s(0, o = c));
  const d = g();
  k(t, d, (c) => s(1, l = c));
  const f = [], z = be("$$ms-gr-antd-react-wrapper"), {
    slotKey: U,
    slotIndex: G,
    subSlotIndex: H
  } = Q() || {}, K = u({
    parent: z,
    props: p,
    target: a,
    slot: d,
    slotKey: U,
    slotIndex: G,
    subSlotIndex: H,
    onDestroy(c) {
      f.push(c);
    }
  });
  ye("$$ms-gr-antd-react-wrapper", K), we(() => {
    p.set(j(n));
  }), he(() => {
    f.forEach((c) => c());
  });
  function q(c) {
    R[c ? "unshift" : "push"](() => {
      o = c, a.set(o);
    });
  }
  function B(c) {
    R[c ? "unshift" : "push"](() => {
      l = c, d.set(l);
    });
  }
  return t.$$set = (c) => {
    s(17, n = E(E({}, n), O(c))), "svelteInit" in c && s(5, u = c.svelteInit), "$$scope" in c && s(6, r = c.$$scope);
  }, n = O(n), [o, l, a, d, i, u, r, e, q, B];
}
class Ie extends se {
  constructor(n) {
    super(), pe(this, n, xe, ve, _e, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, v = window.ms_globals.tree;
function Ce(t) {
  function n(s) {
    const o = g(), l = new Ie({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? v;
          return i.nodes = [...i.nodes, r], F({
            createPortal: S,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((u) => u.svelteInstance !== o), F({
              createPortal: S,
              node: v
            });
          }), r;
        },
        ...s.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(n);
    });
  });
}
function Se(t) {
  const [n, s] = J(() => m(t));
  return N(() => {
    let o = !0;
    return t.subscribe((e) => {
      o && (o = !1, e === n) || s(e);
    });
  }, [t]), n;
}
function Ee(t) {
  const n = C(() => X(t, (s) => s), [t]);
  return Se(n);
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(t) {
  return t ? Object.keys(t).reduce((n, s) => {
    const o = t[s];
    return typeof o == "number" && !Re.includes(s) ? n[s] = o + "px" : n[s] = o, n;
  }, {}) : {};
}
function W(t) {
  const n = t.cloneNode(!0);
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: e,
      type: r,
      useCapture: i
    }) => {
      n.addEventListener(r, e, i);
    });
  });
  const s = Array.from(t.children);
  for (let o = 0; o < s.length; o++) {
    const l = s[o], e = W(l);
    n.replaceChild(e, n.children[o]);
  }
  return n;
}
function Oe(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const Pe = V(({
  slot: t,
  clone: n,
  className: s,
  style: o
}, l) => {
  const e = Y();
  return N(() => {
    var p;
    if (!e.current || !t)
      return;
    let r = t;
    function i() {
      let a = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (a = r.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(l, a), s && a.classList.add(...s.split(" ")), o) {
        const d = ke(o);
        Object.keys(d).forEach((f) => {
          a.style[f] = d[f];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var d;
        r = W(t), r.style.display = "contents", i(), (d = e.current) == null || d.appendChild(r);
      };
      a(), u = new window.MutationObserver(() => {
        var d, f;
        (d = e.current) != null && d.contains(r) && ((f = e.current) == null || f.removeChild(r)), a();
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", i(), (p = e.current) == null || p.appendChild(r);
    return () => {
      var a, d;
      r.style.display = "", (a = e.current) != null && a.contains(r) && ((d = e.current) == null || d.removeChild(r)), u == null || u.disconnect();
    };
  }, [t, n, s, o, l]), I.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function je(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function L(t) {
  return C(() => je(t), [t]);
}
function Fe(t, n) {
  const s = C(() => I.Children.toArray(t).filter((e) => e.props.node && (!e.props.nodeSlotKey || n)).sort((e, r) => {
    if (e.props.node.slotIndex && r.props.node.slotIndex) {
      const i = m(e.props.node.slotIndex) || 0, u = m(r.props.node.slotIndex) || 0;
      return i - u === 0 && e.props.node.subSlotIndex && r.props.node.subSlotIndex ? (m(e.props.node.subSlotIndex) || 0) - (m(r.props.node.subSlotIndex) || 0) : i - u;
    }
    return 0;
  }).map((e) => e.props.node.target), [t, n]);
  return Ee(s);
}
const Ne = Ce(({
  afterChange: t,
  beforeChange: n,
  children: s,
  ...o
}) => {
  const l = L(t), e = L(n), r = Fe(s);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: s
    }), /* @__PURE__ */ _.jsx(Z, {
      ...o,
      afterChange: l,
      beforeChange: e,
      children: r.map((i, u) => /* @__PURE__ */ _.jsx(Pe, {
        clone: !0,
        slot: i
      }, u))
    })]
  });
});
export {
  Ne as Carousel,
  Ne as default
};
