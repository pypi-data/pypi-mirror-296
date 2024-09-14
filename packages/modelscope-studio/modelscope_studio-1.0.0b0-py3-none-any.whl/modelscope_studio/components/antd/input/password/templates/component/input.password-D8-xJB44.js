import { g as Q, w as g } from "./Index-BffyF2su.js";
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
var X = P, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function A(t, r, n) {
  var o, l = {}, e = null, s = null;
  n !== void 0 && (e = "" + n), r.key !== void 0 && (e = "" + r.key), r.ref !== void 0 && (s = r.ref);
  for (o in r) ee.call(r, o) && !re.hasOwnProperty(o) && (l[o] = r[o]);
  if (t && t.defaultProps) for (o in r = t.defaultProps, r) l[o] === void 0 && (l[o] = r[o]);
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
  SvelteComponent: ne,
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
  let r, n;
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
      r = N("svelte-slot"), l && l.c(), D(r, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, r, s), l && l.m(r, null), t[9](r), n = !0;
    },
    p(e, s) {
      l && l.p && (!n || s & /*$$scope*/
      64) && me(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        n ? ce(
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
      n || (h(l, e), n = !0);
    },
    o(e) {
      I(l, e), n = !1;
    },
    d(e) {
      e && b(r), l && l.d(e), t[9](null);
    }
  };
}
function ye(t) {
  let r, n, o, l, e = (
    /*$$slots*/
    t[4].default && O(t)
  );
  return {
    c() {
      r = N("react-portal-target"), n = _e(), e && e.c(), o = ie(), D(r, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      y(s, r, i), t[8](r), y(s, n, i), e && e.m(s, i), y(s, o, i), l = !0;
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
      s && (b(r), b(n), b(o)), t[8](null), e && e.d(s);
    }
  };
}
function j(t) {
  const {
    svelteInit: r,
    ...n
  } = t;
  return n;
}
function he(t, r, n) {
  let o, l, {
    $$slots: e = {},
    $$scope: s
  } = r;
  const i = se(e);
  let {
    svelteInit: f
  } = r;
  const m = g(j(r)), a = g();
  R(t, a, (d) => n(0, o = d));
  const c = g();
  R(t, c, (d) => n(1, l = d));
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
    m.set(j(r));
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
    n(17, r = C(C({}, r), k(d))), "svelteInit" in d && n(5, f = d.svelteInit), "$$scope" in d && n(6, s = d.$$scope);
  }, r = k(r), [o, l, a, c, i, f, s, e, q, G];
}
class xe extends ne {
  constructor(r) {
    super(), fe(this, r, he, ye, ue, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, v = window.ms_globals.tree;
function ve(t) {
  function r(n) {
    const o = g(), l = new xe({
      ...n,
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
        ...n.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(r);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ee(t) {
  return t ? Object.keys(t).reduce((r, n) => {
    const o = t[n];
    return typeof o == "number" && !Ie.includes(n) ? r[n] = o + "px" : r[n] = o, r;
  }, {}) : {};
}
function B(t) {
  const r = t.cloneNode(!0);
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: e,
      type: s,
      useCapture: i
    }) => {
      r.addEventListener(s, e, i);
    });
  });
  const n = Array.from(t.children);
  for (let o = 0; o < n.length; o++) {
    const l = n[o], e = B(l);
    r.replaceChild(e, r.children[o]);
  }
  return r;
}
function Ce(t, r) {
  t && (typeof t == "function" ? t(r) : t.current = r);
}
const p = H(({
  slot: t,
  clone: r,
  className: n,
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
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (a = s.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ce(l, a), n && a.classList.add(...n.split(" ")), o) {
        const c = Ee(o);
        Object.keys(c).forEach((u) => {
          a.style[u] = c[u];
        });
      }
    }
    let f = null;
    if (r && window.MutationObserver) {
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
  }, [t, r, n, o, l]), P.createElement("react-child", {
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
  children: r,
  count: n,
  showCount: o,
  onValueChange: l,
  onChange: e,
  elRef: s,
  ...i
}) => {
  const f = w(n == null ? void 0 : n.strategy), m = w(n == null ? void 0 : n.exceedFormatter), a = w(n == null ? void 0 : n.show), c = w(typeof o == "object" ? o.formatter : void 0);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ _.jsx(V.Password, {
      ...i,
      ref: s,
      onChange: (u) => {
        e == null || e(u), l(u.target.value);
      },
      showCount: typeof o == "object" && c ? {
        formatter: c
      } : o,
      count: {
        ...n,
        exceedFormatter: m,
        strategy: f,
        show: a || (n == null ? void 0 : n.show)
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
  ke as InputPassword,
  ke as default
};
