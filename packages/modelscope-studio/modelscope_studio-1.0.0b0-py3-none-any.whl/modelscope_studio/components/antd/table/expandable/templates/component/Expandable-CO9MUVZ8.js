import { b as J } from "./Index-CH9J9t8x.js";
const A = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useEffect;
function v() {
}
function Z(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
function $(n, ...e) {
  if (n == null) {
    for (const t of e)
      t(void 0);
    return v;
  }
  const s = n.subscribe(...e);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function b(n) {
  let e;
  return $(n, (s) => e = s)(), e;
}
const g = [];
function p(n, e = v) {
  let s;
  const t = /* @__PURE__ */ new Set();
  function o(c) {
    if (Z(n, c) && (n = c, s)) {
      const a = !g.length;
      for (const d of t)
        d[1](), g.push(d, n);
      if (a) {
        for (let d = 0; d < g.length; d += 2)
          g[d][0](g[d + 1]);
        g.length = 0;
      }
    }
  }
  function r(c) {
    o(c(n));
  }
  function i(c, a = v) {
    const d = [c, a];
    return t.add(d), t.size === 1 && (s = e(o, r) || v), c(n), () => {
      t.delete(d), t.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: o,
    update: r,
    subscribe: i
  };
}
const {
  getContext: z,
  setContext: P
} = window.__gradio__svelte__internal, ee = "$$ms-gr-antd-slots-key";
function te() {
  const n = p({});
  return P(ee, n);
}
const ne = "$$ms-gr-antd-context-key";
function re(n) {
  var c;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = W(), s = ie({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  e && e.subscribe((a) => {
    s.slotKey.set(a);
  }), se();
  const t = z(ne), o = ((c = b(t)) == null ? void 0 : c.as_item) || n.as_item, r = t ? o ? b(t)[o] : b(t) : {}, i = p({
    ...n,
    ...r
  });
  return t ? (t.subscribe((a) => {
    const {
      as_item: d
    } = b(i);
    d && (a = a[d]), i.update((u) => ({
      ...u,
      ...a
    }));
  }), [i, (a) => {
    const d = a.as_item ? b(t)[a.as_item] : b(t);
    return i.set({
      ...a,
      ...d
    });
  }]) : [i, (a) => {
    i.set(a);
  }];
}
const M = "$$ms-gr-antd-slot-key";
function se() {
  P(M, p(void 0));
}
function W() {
  return z(M);
}
const oe = "$$ms-gr-antd-component-slot-context-key";
function ie({
  slot: n,
  index: e,
  subIndex: s
}) {
  return P(oe, {
    slotKey: p(n),
    slotIndex: p(e),
    subSlotIndex: p(s)
  });
}
function O(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function le(n) {
  return n && n.__esModule && Object.prototype.hasOwnProperty.call(n, "default") ? n.default : n;
}
var D = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ce = A, ue = Symbol.for("react.element"), ae = Symbol.for("react.fragment"), de = Object.prototype.hasOwnProperty, fe = ce.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, me = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, e, s) {
  var t, o = {}, r = null, i = null;
  s !== void 0 && (r = "" + s), e.key !== void 0 && (r = "" + e.key), e.ref !== void 0 && (i = e.ref);
  for (t in e) de.call(e, t) && !me.hasOwnProperty(t) && (o[t] = e[t]);
  if (n && n.defaultProps) for (t in e = n.defaultProps, e) o[t] === void 0 && (o[t] = e[t]);
  return {
    $$typeof: ue,
    type: n,
    key: r,
    ref: i,
    props: o,
    _owner: fe.current
  };
}
I.Fragment = ae;
I.jsx = G;
I.jsxs = G;
D.exports = I;
var _e = D.exports;
const pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function be(n) {
  return n ? Object.keys(n).reduce((e, s) => {
    const t = n[s];
    return typeof t == "number" && !pe.includes(s) ? e[s] = t + "px" : e[s] = t, e;
  }, {}) : {};
}
function H(n) {
  const e = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((t) => {
    n.getEventListeners(t).forEach(({
      listener: r,
      type: i,
      useCapture: c
    }) => {
      e.addEventListener(i, r, c);
    });
  });
  const s = Array.from(n.children);
  for (let t = 0; t < s.length; t++) {
    const o = s[t], r = H(o);
    e.replaceChild(r, e.children[t]);
  }
  return e;
}
function ge(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const he = Y(({
  slot: n,
  clone: e,
  className: s,
  style: t
}, o) => {
  const r = Q();
  return X(() => {
    var d;
    if (!r.current || !n)
      return;
    let i = n;
    function c() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ge(o, u), s && u.classList.add(...s.split(" ")), t) {
        const f = be(t);
        Object.keys(f).forEach((m) => {
          u.style[m] = f[m];
        });
      }
    }
    let a = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var f;
        i = H(n), i.style.display = "contents", c(), (f = r.current) == null || f.appendChild(i);
      };
      u(), a = new window.MutationObserver(() => {
        var f, m;
        (f = r.current) != null && f.contains(i) && ((m = r.current) == null || m.removeChild(i)), u();
      }), a.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", c(), (d = r.current) == null || d.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = r.current) != null && u.contains(i) && ((f = r.current) == null || f.removeChild(i)), a == null || a.disconnect();
    };
  }, [n, e, s, t, o]), A.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  });
});
function q(n, e) {
  return n ? /* @__PURE__ */ _e.jsx(he, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
var U = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(n) {
  (function() {
    var e = {}.hasOwnProperty;
    function s() {
      for (var r = "", i = 0; i < arguments.length; i++) {
        var c = arguments[i];
        c && (r = o(r, t(c)));
      }
      return r;
    }
    function t(r) {
      if (typeof r == "string" || typeof r == "number")
        return r;
      if (typeof r != "object")
        return "";
      if (Array.isArray(r))
        return s.apply(null, r);
      if (r.toString !== Object.prototype.toString && !r.toString.toString().includes("[native code]"))
        return r.toString();
      var i = "";
      for (var c in r)
        e.call(r, c) && r[c] && (i = o(i, c));
      return i;
    }
    function o(r, i) {
      return i ? r ? r + " " + i : r + i : r;
    }
    n.exports ? (s.default = s, n.exports = s) : window.classNames = s;
  })();
})(U);
var xe = U.exports;
const ye = /* @__PURE__ */ le(xe), {
  getContext: we,
  setContext: Ce
} = window.__gradio__svelte__internal;
function Ee(n) {
  const e = `$$ms-gr-antd-${n}-context-key`;
  function s(o = ["default"]) {
    const r = o.reduce((i, c) => (i[c] = p([]), i), {});
    return Ce(e, {
      itemsMap: r,
      allowedSlots: o
    }), r;
  }
  function t() {
    const {
      itemsMap: o,
      allowedSlots: r
    } = we(e);
    return function(i, c, a) {
      o && (i ? o[i].update((d) => {
        const u = [...d];
        return r.includes(i) ? u[c] = a : u[c] = void 0, u;
      }) : r.includes("default") && o.default.update((d) => {
        const u = [...d];
        return u[c] = a, u;
      }));
    };
  }
  return {
    getItems: s,
    getSetItemFn: t
  };
}
const {
  getItems: Me,
  getSetItemFn: Se
} = Ee("table-expandable"), {
  SvelteComponent: ve,
  check_outros: Re,
  component_subscribe: S,
  create_slot: Ie,
  detach: Oe,
  empty: ke,
  flush: _,
  get_all_dirty_from_scope: Pe,
  get_slot_changes: je,
  group_outros: Ne,
  init: Fe,
  insert: Ke,
  safe_not_equal: Le,
  transition_in: R,
  transition_out: k,
  update_slot_base: qe
} = window.__gradio__svelte__internal;
function T(n) {
  let e;
  const s = (
    /*#slots*/
    n[18].default
  ), t = Ie(
    s,
    n,
    /*$$scope*/
    n[17],
    null
  );
  return {
    c() {
      t && t.c();
    },
    m(o, r) {
      t && t.m(o, r), e = !0;
    },
    p(o, r) {
      t && t.p && (!e || r & /*$$scope*/
      131072) && qe(
        t,
        s,
        o,
        /*$$scope*/
        o[17],
        e ? je(
          s,
          /*$$scope*/
          o[17],
          r,
          null
        ) : Pe(
          /*$$scope*/
          o[17]
        ),
        null
      );
    },
    i(o) {
      e || (R(t, o), e = !0);
    },
    o(o) {
      k(t, o), e = !1;
    },
    d(o) {
      t && t.d(o);
    }
  };
}
function Te(n) {
  let e, s, t = (
    /*$mergedProps*/
    n[0].visible && T(n)
  );
  return {
    c() {
      t && t.c(), e = ke();
    },
    m(o, r) {
      t && t.m(o, r), Ke(o, e, r), s = !0;
    },
    p(o, [r]) {
      /*$mergedProps*/
      o[0].visible ? t ? (t.p(o, r), r & /*$mergedProps*/
      1 && R(t, 1)) : (t = T(o), t.c(), R(t, 1), t.m(e.parentNode, e)) : t && (Ne(), k(t, 1, 1, () => {
        t = null;
      }), Re());
    },
    i(o) {
      s || (R(t), s = !0);
    },
    o(o) {
      k(t), s = !1;
    },
    d(o) {
      o && Oe(e), t && t.d(o);
    }
  };
}
function Ae(n, e, s) {
  let t, o, r, i, {
    $$slots: c = {},
    $$scope: a
  } = e, {
    gradio: d
  } = e, {
    props: u = {}
  } = e;
  const f = p(u);
  S(n, f, (l) => s(16, i = l));
  let {
    _internal: m = {}
  } = e, {
    as_item: x
  } = e, {
    value: h
  } = e, {
    visible: y = !0
  } = e, {
    elem_id: w = ""
  } = e, {
    elem_classes: C = []
  } = e, {
    elem_style: E = {}
  } = e;
  const j = W();
  S(n, j, (l) => s(15, r = l));
  const [N, V] = re({
    gradio: d,
    props: i,
    _internal: m,
    visible: y,
    elem_id: w,
    elem_classes: C,
    elem_style: E,
    as_item: x,
    value: h
  });
  S(n, N, (l) => s(0, t = l));
  const F = te();
  S(n, F, (l) => s(14, o = l));
  const B = Se();
  return n.$$set = (l) => {
    "gradio" in l && s(6, d = l.gradio), "props" in l && s(7, u = l.props), "_internal" in l && s(8, m = l._internal), "as_item" in l && s(9, x = l.as_item), "value" in l && s(5, h = l.value), "visible" in l && s(10, y = l.visible), "elem_id" in l && s(11, w = l.elem_id), "elem_classes" in l && s(12, C = l.elem_classes), "elem_style" in l && s(13, E = l.elem_style), "$$scope" in l && s(17, a = l.$$scope);
  }, n.$$.update = () => {
    if (n.$$.dirty & /*props*/
    128 && f.update((l) => ({
      ...l,
      ...u
    })), n.$$.dirty & /*$mergedProps, $slotKey, $slots*/
    49153) {
      const l = J(t);
      B(r, t._internal.index || 0, {
        props: {
          style: t.elem_style,
          className: ye(t.elem_classes, "ms-gr-antd-table-expandable"),
          id: t.elem_id,
          expandedRowKeys: t.value,
          ...t.props,
          ...l,
          onExpandedRowsChange: (K) => {
            var L;
            (L = l == null ? void 0 : l.onExpandedRowsChange) == null || L.call(l, K), s(5, h = K);
          },
          expandedRowClassName: O(t.props.expandedRowClassName),
          expandedRowRender: O(t.props.expandedRowRender),
          rowExpandable: O(t.props.rowExpandable),
          expandIcon: o.expandIcon ? () => q(o.expandIcon) : t.props.expandIcon,
          columnTitle: q(o.columnTitle) || t.props.columnTitle
        },
        slots: {}
      });
    }
    n.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    81760 && V({
      gradio: d,
      props: i,
      _internal: m,
      visible: y,
      elem_id: w,
      elem_classes: C,
      elem_style: E,
      as_item: x,
      value: h
    });
  }, [t, f, j, N, F, h, d, u, m, x, y, w, C, E, o, r, i, a, c];
}
class We extends ve {
  constructor(e) {
    super(), Fe(this, e, Ae, Te, Le, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      value: 5,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), _();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(e) {
    this.$$set({
      props: e
    }), _();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), _();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), _();
  }
  get value() {
    return this.$$.ctx[5];
  }
  set value(e) {
    this.$$set({
      value: e
    }), _();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), _();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), _();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), _();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), _();
  }
}
export {
  We as default
};
