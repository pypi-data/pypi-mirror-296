import { g as Q, w as p } from "./Index-DDEDvU9U.js";
const L = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useEffect, K = window.ms_globals.React.useMemo, E = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.internalContext.FormItemContext, X = window.ms_globals.antd.Radio;
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
var Z = L, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(l, t, o) {
  var r, s = {}, e = null, n = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (n = t.ref);
  for (r in t) te.call(t, r) && !re.hasOwnProperty(r) && (s[r] = t[r]);
  if (l && l.defaultProps) for (r in t = l.defaultProps, t) s[r] === void 0 && (s[r] = t[r]);
  return {
    $$typeof: $,
    type: l,
    key: e,
    ref: n,
    props: s,
    _owner: ne.current
  };
}
h.Fragment = ee;
h.jsx = F;
h.jsxs = F;
N.exports = h;
var m = N.exports;
const {
  SvelteComponent: oe,
  assign: I,
  binding_callbacks: R,
  check_outros: le,
  component_subscribe: C,
  compute_slots: se,
  create_slot: ce,
  detach: g,
  element: D,
  empty: ie,
  exclude_internal_props: k,
  get_all_dirty_from_scope: ae,
  get_slot_changes: ue,
  group_outros: de,
  init: fe,
  insert: b,
  safe_not_equal: _e,
  set_custom_element_data: G,
  space: me,
  transition_in: w,
  transition_out: x,
  update_slot_base: pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: be,
  onDestroy: we,
  setContext: he
} = window.__gradio__svelte__internal;
function O(l) {
  let t, o;
  const r = (
    /*#slots*/
    l[7].default
  ), s = ce(
    r,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), s && s.c(), G(t, "class", "svelte-1rt0kpf");
    },
    m(e, n) {
      b(e, t, n), s && s.m(t, null), l[9](t), o = !0;
    },
    p(e, n) {
      s && s.p && (!o || n & /*$$scope*/
      64) && pe(
        s,
        r,
        e,
        /*$$scope*/
        e[6],
        o ? ue(
          r,
          /*$$scope*/
          e[6],
          n,
          null
        ) : ae(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (w(s, e), o = !0);
    },
    o(e) {
      x(s, e), o = !1;
    },
    d(e) {
      e && g(t), s && s.d(e), l[9](null);
    }
  };
}
function ve(l) {
  let t, o, r, s, e = (
    /*$$slots*/
    l[4].default && O(l)
  );
  return {
    c() {
      t = D("react-portal-target"), o = me(), e && e.c(), r = ie(), G(t, "class", "svelte-1rt0kpf");
    },
    m(n, c) {
      b(n, t, c), l[8](t), b(n, o, c), e && e.m(n, c), b(n, r, c), s = !0;
    },
    p(n, [c]) {
      /*$$slots*/
      n[4].default ? e ? (e.p(n, c), c & /*$$slots*/
      16 && w(e, 1)) : (e = O(n), e.c(), w(e, 1), e.m(r.parentNode, r)) : e && (de(), x(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(n) {
      s || (w(e), s = !0);
    },
    o(n) {
      x(e), s = !1;
    },
    d(n) {
      n && (g(t), g(o), g(r)), l[8](null), e && e.d(n);
    }
  };
}
function S(l) {
  const {
    svelteInit: t,
    ...o
  } = l;
  return o;
}
function ye(l, t, o) {
  let r, s, {
    $$slots: e = {},
    $$scope: n
  } = t;
  const c = se(e);
  let {
    svelteInit: d
  } = t;
  const _ = p(S(t)), i = p();
  C(l, i, (u) => o(0, r = u));
  const a = p();
  C(l, a, (u) => o(1, s = u));
  const f = [], v = be("$$ms-gr-antd-react-wrapper"), {
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T
  } = Q() || {}, U = d({
    parent: v,
    props: _,
    target: i,
    slot: a,
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T,
    onDestroy(u) {
      f.push(u);
    }
  });
  he("$$ms-gr-antd-react-wrapper", U), ge(() => {
    _.set(S(t));
  }), we(() => {
    f.forEach((u) => u());
  });
  function q(u) {
    R[u ? "unshift" : "push"](() => {
      r = u, i.set(r);
    });
  }
  function H(u) {
    R[u ? "unshift" : "push"](() => {
      s = u, a.set(s);
    });
  }
  return l.$$set = (u) => {
    o(17, t = I(I({}, t), k(u))), "svelteInit" in u && o(5, d = u.svelteInit), "$$scope" in u && o(6, n = u.$$scope);
  }, t = k(t), [r, s, i, a, c, d, n, e, q, H];
}
class xe extends oe {
  constructor(t) {
    super(), fe(this, t, ye, ve, _e, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, y = window.ms_globals.tree;
function Ee(l) {
  function t(o) {
    const r = p(), s = new xe({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const n = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? y;
          return c.nodes = [...c.nodes, n], j({
            createPortal: E,
            node: y
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((d) => d.svelteInstance !== r), j({
              createPortal: E,
              node: y
            });
          }), n;
        },
        ...o.props
      }
    });
    return r.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(l) {
  return l ? Object.keys(l).reduce((t, o) => {
    const r = l[o];
    return typeof r == "number" && !Ie.includes(o) ? t[o] = r + "px" : t[o] = r, t;
  }, {}) : {};
}
function M(l) {
  const t = l.cloneNode(!0);
  Object.keys(l.getEventListeners()).forEach((r) => {
    l.getEventListeners(r).forEach(({
      listener: e,
      type: n,
      useCapture: c
    }) => {
      t.addEventListener(n, e, c);
    });
  });
  const o = Array.from(l.children);
  for (let r = 0; r < o.length; r++) {
    const s = o[r], e = M(s);
    t.replaceChild(e, t.children[r]);
  }
  return t;
}
function Ce(l, t) {
  l && (typeof l == "function" ? l(t) : l.current = t);
}
const P = B(({
  slot: l,
  clone: t,
  className: o,
  style: r
}, s) => {
  const e = J();
  return Y(() => {
    var _;
    if (!e.current || !l)
      return;
    let n = l;
    function c() {
      let i = n;
      if (n.tagName.toLowerCase() === "svelte-slot" && n.children.length === 1 && n.children[0] && (i = n.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Ce(s, i), o && i.classList.add(...o.split(" ")), r) {
        const a = Re(r);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var a;
        n = M(l), n.style.display = "contents", c(), (a = e.current) == null || a.appendChild(n);
      };
      i(), d = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(n) && ((f = e.current) == null || f.removeChild(n)), i();
      }), d.observe(l, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      n.style.display = "contents", c(), (_ = e.current) == null || _.appendChild(n);
    return () => {
      var i, a;
      n.style.display = "", (i = e.current) != null && i.contains(n) && ((a = e.current) == null || a.removeChild(n)), d == null || d.disconnect();
    };
  }, [l, t, o, r, s]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function W(l, t) {
  return l.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const r = {
      ...o.props
    };
    let s = r;
    Object.keys(o.slots).forEach((n) => {
      if (!o.slots[n] || !(o.slots[n] instanceof Element) && !o.slots[n].el)
        return;
      const c = n.split(".");
      c.forEach((f, v) => {
        s[f] || (s[f] = {}), v !== c.length - 1 && (s = r[f]);
      });
      const d = o.slots[n];
      let _, i, a = !1;
      d instanceof Element ? _ = d : (_ = d.el, i = d.callback, a = d.clone || !1), s[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ m.jsx(P, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ m.jsx(P, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      }) : s[c[c.length - 1]], s = r;
    });
    const e = "children";
    return o[e] && (r[e] = W(o[e], t)), r;
  });
}
const Oe = Ee(({
  onValueChange: l,
  onChange: t,
  elRef: o,
  optionItems: r,
  options: s,
  children: e,
  ...n
}) => /* @__PURE__ */ m.jsx(m.Fragment, {
  children: /* @__PURE__ */ m.jsx(X.Group, {
    ...n,
    ref: o,
    options: K(() => s || W(r), [r, s]),
    onChange: (c) => {
      t == null || t(c), l(c.target.value);
    },
    children: /* @__PURE__ */ m.jsx(V.Provider, {
      value: null,
      children: e
    })
  })
}));
export {
  Oe as RadioGroup,
  Oe as default
};
