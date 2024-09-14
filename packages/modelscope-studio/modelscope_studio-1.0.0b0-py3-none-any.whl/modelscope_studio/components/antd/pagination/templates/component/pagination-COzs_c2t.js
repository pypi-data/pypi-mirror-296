import { g as K, w as m } from "./Index-_ElhcX7Q.js";
const P = window.ms_globals.React, q = window.ms_globals.React.forwardRef, z = window.ms_globals.React.useRef, G = window.ms_globals.React.useEffect, H = window.ms_globals.React.useMemo, v = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.Pagination;
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
var Y = P, V = Symbol.for("react.element"), X = Symbol.for("react.fragment"), Z = Object.prototype.hasOwnProperty, $ = Y.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(n, t, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (r in t) Z.call(t, r) && !ee.hasOwnProperty(r) && (l[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: V,
    type: n,
    key: e,
    ref: o,
    props: l,
    _owner: $.current
  };
}
b.Fragment = X;
b.jsx = j;
b.jsxs = j;
L.exports = b;
var E = L.exports;
const {
  SvelteComponent: te,
  assign: x,
  binding_callbacks: I,
  check_outros: ne,
  component_subscribe: k,
  compute_slots: oe,
  create_slot: re,
  detach: p,
  element: F,
  empty: se,
  exclude_internal_props: R,
  get_all_dirty_from_scope: le,
  get_slot_changes: ie,
  group_outros: ce,
  init: ue,
  insert: g,
  safe_not_equal: ae,
  set_custom_element_data: N,
  space: de,
  transition_in: w,
  transition_out: y,
  update_slot_base: fe
} = window.__gradio__svelte__internal, {
  beforeUpdate: _e,
  getContext: me,
  onDestroy: pe,
  setContext: ge
} = window.__gradio__svelte__internal;
function C(n) {
  let t, s;
  const r = (
    /*#slots*/
    n[7].default
  ), l = re(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = F("svelte-slot"), l && l.c(), N(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      g(e, t, o), l && l.m(t, null), n[9](t), s = !0;
    },
    p(e, o) {
      l && l.p && (!s || o & /*$$scope*/
      64) && fe(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? ie(
          r,
          /*$$scope*/
          e[6],
          o,
          null
        ) : le(
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
      e && p(t), l && l.d(e), n[9](null);
    }
  };
}
function we(n) {
  let t, s, r, l, e = (
    /*$$slots*/
    n[4].default && C(n)
  );
  return {
    c() {
      t = F("react-portal-target"), s = de(), e && e.c(), r = se(), N(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      g(o, t, i), n[8](t), g(o, s, i), e && e.m(o, i), g(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && w(e, 1)) : (e = C(o), e.c(), w(e, 1), e.m(r.parentNode, r)) : e && (ce(), y(e, 1, 1, () => {
        e = null;
      }), ne());
    },
    i(o) {
      l || (w(e), l = !0);
    },
    o(o) {
      y(e), l = !1;
    },
    d(o) {
      o && (p(t), p(s), p(r)), n[8](null), e && e.d(o);
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
function be(n, t, s) {
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const i = oe(e);
  let {
    svelteInit: d
  } = t;
  const _ = m(S(t)), c = m();
  k(n, c, (u) => s(0, r = u));
  const a = m();
  k(n, a, (u) => s(1, l = u));
  const f = [], M = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: T,
    slotIndex: W,
    subSlotIndex: A
  } = K() || {}, B = d({
    parent: M,
    props: _,
    target: c,
    slot: a,
    slotKey: T,
    slotIndex: W,
    subSlotIndex: A,
    onDestroy(u) {
      f.push(u);
    }
  });
  ge("$$ms-gr-antd-react-wrapper", B), _e(() => {
    _.set(S(t));
  }), pe(() => {
    f.forEach((u) => u());
  });
  function J(u) {
    I[u ? "unshift" : "push"](() => {
      r = u, c.set(r);
    });
  }
  function U(u) {
    I[u ? "unshift" : "push"](() => {
      l = u, a.set(l);
    });
  }
  return n.$$set = (u) => {
    s(17, t = x(x({}, t), R(u))), "svelteInit" in u && s(5, d = u.svelteInit), "$$scope" in u && s(6, o = u.$$scope);
  }, t = R(t), [r, l, c, a, i, d, o, e, J, U];
}
class he extends te {
  constructor(t) {
    super(), ue(this, t, be, we, ae, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, h = window.ms_globals.tree;
function ye(n) {
  function t(s) {
    const r = m(), l = new he({
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
          }, i = e.parent ?? h;
          return i.nodes = [...i.nodes, o], O({
            createPortal: v,
            node: h
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), O({
              createPortal: v,
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
      s(t);
    });
  });
}
const ve = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ee(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const r = n[s];
    return typeof r == "number" && !ve.includes(s) ? t[s] = r + "px" : t[s] = r, t;
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
function xe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Ie = q(({
  slot: n,
  clone: t,
  className: s,
  style: r
}, l) => {
  const e = z();
  return G(() => {
    var _;
    if (!e.current || !n)
      return;
    let o = n;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), xe(l, c), s && c.classList.add(...s.split(" ")), r) {
        const a = Ee(r);
        Object.keys(a).forEach((f) => {
          c.style[f] = a[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var a;
        o = D(n), o.style.display = "contents", i(), (a = e.current) == null || a.appendChild(o);
      };
      c(), d = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(o) && ((f = e.current) == null || f.removeChild(o)), c();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (_ = e.current) == null || _.appendChild(o);
    return () => {
      var c, a;
      o.style.display = "", (c = e.current) != null && c.contains(o) && ((a = e.current) == null || a.removeChild(o)), d == null || d.disconnect();
    };
  }, [n, t, s, r, l]), P.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function ke(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Re(n) {
  return H(() => ke(n), [n]);
}
const Se = ye(({
  slots: n,
  onValueChange: t,
  showTotal: s,
  showQuickJumper: r,
  onChange: l,
  ...e
}) => {
  const o = Re(s);
  return /* @__PURE__ */ E.jsx(Q, {
    ...e,
    showTotal: s ? o : void 0,
    onChange: (i, d) => {
      t(i, d), l == null || l(i, d);
    },
    showQuickJumper: n["showQuickJumper.goButton"] ? {
      goButton: /* @__PURE__ */ E.jsx(Ie, {
        slot: n["showQuickJumper.goButton"]
      })
    } : r
  });
});
export {
  Se as Pagination,
  Se as default
};
