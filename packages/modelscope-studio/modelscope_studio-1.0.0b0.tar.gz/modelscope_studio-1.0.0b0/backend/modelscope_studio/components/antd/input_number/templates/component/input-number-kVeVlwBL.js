import { g as Q, w } from "./Index-BUaYenWu.js";
const N = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, J = window.ms_globals.React.useEffect, Y = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.InputNumber;
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
var X = N, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function L(e, n, s) {
  var o, l = {}, t = null, r = null;
  s !== void 0 && (t = "" + s), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (r = n.ref);
  for (o in n) ee.call(n, o) && !ne.hasOwnProperty(o) && (l[o] = n[o]);
  if (e && e.defaultProps) for (o in n = e.defaultProps, n) l[o] === void 0 && (l[o] = n[o]);
  return {
    $$typeof: Z,
    type: e,
    key: t,
    ref: r,
    props: l,
    _owner: te.current
  };
}
h.Fragment = $;
h.jsx = L;
h.jsxs = L;
F.exports = h;
var f = F.exports;
const {
  SvelteComponent: oe,
  assign: E,
  binding_callbacks: R,
  check_outros: re,
  component_subscribe: S,
  compute_slots: se,
  create_slot: le,
  detach: g,
  element: A,
  empty: ie,
  exclude_internal_props: C,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ue,
  group_outros: ae,
  init: de,
  insert: b,
  safe_not_equal: fe,
  set_custom_element_data: D,
  space: _e,
  transition_in: y,
  transition_out: v,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: we,
  onDestroy: ge,
  setContext: be
} = window.__gradio__svelte__internal;
function j(e) {
  let n, s;
  const o = (
    /*#slots*/
    e[7].default
  ), l = le(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = A("svelte-slot"), l && l.c(), D(n, "class", "svelte-1rt0kpf");
    },
    m(t, r) {
      b(t, n, r), l && l.m(n, null), e[9](n), s = !0;
    },
    p(t, r) {
      l && l.p && (!s || r & /*$$scope*/
      64) && me(
        l,
        o,
        t,
        /*$$scope*/
        t[6],
        s ? ue(
          o,
          /*$$scope*/
          t[6],
          r,
          null
        ) : ce(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      s || (y(l, t), s = !0);
    },
    o(t) {
      v(l, t), s = !1;
    },
    d(t) {
      t && g(n), l && l.d(t), e[9](null);
    }
  };
}
function ye(e) {
  let n, s, o, l, t = (
    /*$$slots*/
    e[4].default && j(e)
  );
  return {
    c() {
      n = A("react-portal-target"), s = _e(), t && t.c(), o = ie(), D(n, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      b(r, n, i), e[8](n), b(r, s, i), t && t.m(r, i), b(r, o, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? t ? (t.p(r, i), i & /*$$slots*/
      16 && y(t, 1)) : (t = j(r), t.c(), y(t, 1), t.m(o.parentNode, o)) : t && (ae(), v(t, 1, 1, () => {
        t = null;
      }), re());
    },
    i(r) {
      l || (y(t), l = !0);
    },
    o(r) {
      v(t), l = !1;
    },
    d(r) {
      r && (g(n), g(s), g(o)), e[8](null), t && t.d(r);
    }
  };
}
function k(e) {
  const {
    svelteInit: n,
    ...s
  } = e;
  return s;
}
function he(e, n, s) {
  let o, l, {
    $$slots: t = {},
    $$scope: r
  } = n;
  const i = se(t);
  let {
    svelteInit: d
  } = n;
  const m = w(k(n)), c = w();
  S(e, c, (u) => s(0, o = u));
  const a = w();
  S(e, a, (u) => s(1, l = u));
  const _ = [], M = we("$$ms-gr-antd-react-wrapper"), {
    slotKey: W,
    slotIndex: z,
    subSlotIndex: T
  } = Q() || {}, U = d({
    parent: M,
    props: m,
    target: c,
    slot: a,
    slotKey: W,
    slotIndex: z,
    subSlotIndex: T,
    onDestroy(u) {
      _.push(u);
    }
  });
  be("$$ms-gr-antd-react-wrapper", U), pe(() => {
    m.set(k(n));
  }), ge(() => {
    _.forEach((u) => u());
  });
  function q(u) {
    R[u ? "unshift" : "push"](() => {
      o = u, c.set(o);
    });
  }
  function G(u) {
    R[u ? "unshift" : "push"](() => {
      l = u, a.set(l);
    });
  }
  return e.$$set = (u) => {
    s(17, n = E(E({}, n), C(u))), "svelteInit" in u && s(5, d = u.svelteInit), "$$scope" in u && s(6, r = u.$$scope);
  }, n = C(n), [o, l, c, a, i, d, r, t, q, G];
}
class xe extends oe {
  constructor(n) {
    super(), de(this, n, he, ye, fe, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, x = window.ms_globals.tree;
function ve(e) {
  function n(s) {
    const o = w(), l = new xe({
      ...s,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? x;
          return i.nodes = [...i.nodes, r], O({
            createPortal: I,
            node: x
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== o), O({
              createPortal: I,
              node: x
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
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ee(e) {
  return e ? Object.keys(e).reduce((n, s) => {
    const o = e[s];
    return typeof o == "number" && !Ie.includes(s) ? n[s] = o + "px" : n[s] = o, n;
  }, {}) : {};
}
function B(e) {
  const n = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: t,
      type: r,
      useCapture: i
    }) => {
      n.addEventListener(r, t, i);
    });
  });
  const s = Array.from(e.children);
  for (let o = 0; o < s.length; o++) {
    const l = s[o], t = B(l);
    n.replaceChild(t, n.children[o]);
  }
  return n;
}
function Re(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const p = H(({
  slot: e,
  clone: n,
  className: s,
  style: o
}, l) => {
  const t = K();
  return J(() => {
    var m;
    if (!t.current || !e)
      return;
    let r = e;
    function i() {
      let c = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (c = r.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Re(l, c), s && c.classList.add(...s.split(" ")), o) {
        const a = Ee(o);
        Object.keys(a).forEach((_) => {
          c.style[_] = a[_];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var a;
        r = B(e), r.style.display = "contents", i(), (a = t.current) == null || a.appendChild(r);
      };
      c(), d = new window.MutationObserver(() => {
        var a, _;
        (a = t.current) != null && a.contains(r) && ((_ = t.current) == null || _.removeChild(r)), c();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", i(), (m = t.current) == null || m.appendChild(r);
    return () => {
      var c, a;
      r.style.display = "", (c = t.current) != null && c.contains(r) && ((a = t.current) == null || a.removeChild(r)), d == null || d.disconnect();
    };
  }, [e, n, s, o, l]), N.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function Se(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function P(e) {
  return Y(() => Se(e), [e]);
}
const je = ve(({
  slots: e,
  children: n,
  onValueChange: s,
  onChange: o,
  formatter: l,
  parser: t,
  elRef: r,
  ...i
}) => {
  const d = P(l), m = P(t);
  return /* @__PURE__ */ f.jsxs(f.Fragment, {
    children: [/* @__PURE__ */ f.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ f.jsx(V, {
      ...i,
      ref: r,
      onChange: (c) => {
        o == null || o(c), s(c);
      },
      parser: m,
      formatter: d,
      controls: e["controls.upIcon"] || e["controls.downIcon"] ? {
        upIcon: e["controls.upIcon"] ? /* @__PURE__ */ f.jsx(p, {
          slot: e["controls.upIcon"]
        }) : typeof i.controls == "object" ? i.controls.upIcon : void 0,
        downIcon: e["controls.downIcon"] ? /* @__PURE__ */ f.jsx(p, {
          slot: e["controls.downIcon"]
        }) : typeof i.controls == "object" ? i.controls.downIcon : void 0
      } : i.controls,
      addonAfter: e.addonAfter ? /* @__PURE__ */ f.jsx(p, {
        slot: e.addonAfter
      }) : i.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ f.jsx(p, {
        slot: e.addonBefore
      }) : i.addonBefore,
      prefix: e.prefix ? /* @__PURE__ */ f.jsx(p, {
        slot: e.prefix
      }) : i.prefix,
      suffix: e.suffix ? /* @__PURE__ */ f.jsx(p, {
        slot: e.suffix
      }) : i.suffix
    })]
  });
});
export {
  je as InputNumber,
  je as default
};
