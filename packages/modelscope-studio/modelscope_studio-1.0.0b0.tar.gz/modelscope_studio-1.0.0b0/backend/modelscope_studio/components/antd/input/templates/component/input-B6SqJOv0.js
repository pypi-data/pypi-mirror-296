import { g as Q, w as g } from "./Index-DUz_vPbc.js";
const P = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, J = window.ms_globals.React.useEffect, Y = window.ms_globals.React.useMemo, E = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Input;
var L = {
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
var X = P, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function A(t, n, r) {
  var o, l = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (o in n) ee.call(n, o) && !ne.hasOwnProperty(o) && (l[o] = n[o]);
  if (t && t.defaultProps) for (o in n = t.defaultProps, n) l[o] === void 0 && (l[o] = n[o]);
  return {
    $$typeof: Z,
    type: t,
    key: e,
    ref: s,
    props: l,
    _owner: te.current
  };
}
x.Fragment = $;
x.jsx = A;
x.jsxs = A;
L.exports = x;
var _ = L.exports;
const {
  SvelteComponent: re,
  assign: C,
  binding_callbacks: S,
  check_outros: oe,
  component_subscribe: R,
  compute_slots: se,
  create_slot: le,
  detach: b,
  element: N,
  empty: ie,
  exclude_internal_props: k,
  get_all_dirty_from_scope: ae,
  get_slot_changes: ce,
  group_outros: de,
  init: fe,
  insert: y,
  safe_not_equal: ue,
  set_custom_element_data: D,
  space: _e,
  transition_in: h,
  transition_out: I,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: we,
  onDestroy: ge,
  setContext: be
} = window.__gradio__svelte__internal;
function O(t) {
  let n, r;
  const o = (
    /*#slots*/
    t[7].default
  ), l = le(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = N("svelte-slot"), l && l.c(), D(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, n, s), l && l.m(n, null), t[9](n), r = !0;
    },
    p(e, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && me(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        r ? ce(
          o,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ae(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (h(l, e), r = !0);
    },
    o(e) {
      I(l, e), r = !1;
    },
    d(e) {
      e && b(n), l && l.d(e), t[9](null);
    }
  };
}
function ye(t) {
  let n, r, o, l, e = (
    /*$$slots*/
    t[4].default && O(t)
  );
  return {
    c() {
      n = N("react-portal-target"), r = _e(), e && e.c(), o = ie(), D(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      y(s, n, i), t[8](n), y(s, r, i), e && e.m(s, i), y(s, o, i), l = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = O(s), e.c(), h(e, 1), e.m(o.parentNode, o)) : e && (de(), I(e, 1, 1, () => {
        e = null;
      }), oe());
    },
    i(s) {
      l || (h(e), l = !0);
    },
    o(s) {
      I(e), l = !1;
    },
    d(s) {
      s && (b(n), b(r), b(o)), t[8](null), e && e.d(s);
    }
  };
}
function j(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function he(t, n, r) {
  let o, l, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const i = se(e);
  let {
    svelteInit: f
  } = n;
  const m = g(j(n)), a = g();
  R(t, a, (d) => r(0, o = d));
  const c = g();
  R(t, c, (d) => r(1, l = d));
  const u = [], M = we("$$ms-gr-antd-react-wrapper"), {
    slotKey: W,
    slotIndex: z,
    subSlotIndex: T
  } = Q() || {}, U = f({
    parent: M,
    props: m,
    target: a,
    slot: c,
    slotKey: W,
    slotIndex: z,
    subSlotIndex: T,
    onDestroy(d) {
      u.push(d);
    }
  });
  be("$$ms-gr-antd-react-wrapper", U), pe(() => {
    m.set(j(n));
  }), ge(() => {
    u.forEach((d) => d());
  });
  function q(d) {
    S[d ? "unshift" : "push"](() => {
      o = d, a.set(o);
    });
  }
  function G(d) {
    S[d ? "unshift" : "push"](() => {
      l = d, c.set(l);
    });
  }
  return t.$$set = (d) => {
    r(17, n = C(C({}, n), k(d))), "svelteInit" in d && r(5, f = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, n = k(n), [o, l, a, c, i, f, s, e, q, G];
}
class xe extends re {
  constructor(n) {
    super(), fe(this, n, he, ye, ue, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, v = window.ms_globals.tree;
function ve(t) {
  function n(r) {
    const o = g(), l = new xe({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
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
          return i.nodes = [...i.nodes, s], F({
            createPortal: E,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((f) => f.svelteInstance !== o), F({
              createPortal: E,
              node: v
            });
          }), s;
        },
        ...r.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ee(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const o = t[r];
    return typeof o == "number" && !Ie.includes(r) ? n[r] = o + "px" : n[r] = o, n;
  }, {}) : {};
}
function B(t) {
  const n = t.cloneNode(!0);
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: e,
      type: s,
      useCapture: i
    }) => {
      n.addEventListener(s, e, i);
    });
  });
  const r = Array.from(t.children);
  for (let o = 0; o < r.length; o++) {
    const l = r[o], e = B(l);
    n.replaceChild(e, n.children[o]);
  }
  return n;
}
function Ce(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const p = H(({
  slot: t,
  clone: n,
  className: r,
  style: o
}, l) => {
  const e = K();
  return J(() => {
    var m;
    if (!e.current || !t)
      return;
    let s = t;
    function i() {
      let a = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (a = s.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ce(l, a), r && a.classList.add(...r.split(" ")), o) {
        const c = Ee(o);
        Object.keys(c).forEach((u) => {
          a.style[u] = c[u];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var c;
        s = B(t), s.style.display = "contents", i(), (c = e.current) == null || c.appendChild(s);
      };
      a(), f = new window.MutationObserver(() => {
        var c, u;
        (c = e.current) != null && c.contains(s) && ((u = e.current) == null || u.removeChild(s)), a();
      }), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      s.style.display = "contents", i(), (m = e.current) == null || m.appendChild(s);
    return () => {
      var a, c;
      s.style.display = "", (a = e.current) != null && a.contains(s) && ((c = e.current) == null || c.removeChild(s)), f == null || f.disconnect();
    };
  }, [t, n, r, o, l]), P.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Se(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function w(t) {
  return Y(() => Se(t), [t]);
}
const ke = ve(({
  slots: t,
  children: n,
  count: r,
  showCount: o,
  onValueChange: l,
  onChange: e,
  elRef: s,
  ...i
}) => {
  const f = w(r == null ? void 0 : r.strategy), m = w(r == null ? void 0 : r.exceedFormatter), a = w(r == null ? void 0 : r.show), c = w(typeof o == "object" ? o.formatter : void 0);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ _.jsx(V, {
      ...i,
      ref: s,
      onChange: (u) => {
        e == null || e(u), l(u.target.value);
      },
      showCount: typeof o == "object" && c ? {
        formatter: c
      } : o,
      count: {
        ...r,
        exceedFormatter: m,
        strategy: f,
        show: a || (r == null ? void 0 : r.show)
      },
      addonAfter: t.addonAfter ? /* @__PURE__ */ _.jsx(p, {
        slot: t.addonAfter
      }) : i.addonAfter,
      addonBefore: t.addonBefore ? /* @__PURE__ */ _.jsx(p, {
        slot: t.addonBefore
      }) : i.addonBefore,
      allowClear: t["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ _.jsx(p, {
          slot: t["allowClear.clearIcon"]
        })
      } : i.allowClear,
      prefix: t.prefix ? /* @__PURE__ */ _.jsx(p, {
        slot: t.prefix
      }) : i.prefix,
      suffix: t.suffix ? /* @__PURE__ */ _.jsx(p, {
        slot: t.suffix
      }) : i.suffix
    })]
  });
});
export {
  ke as Input,
  ke as default
};
