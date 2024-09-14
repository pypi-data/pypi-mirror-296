import { b as ee } from "./Index-D3T3Ddee.js";
const M = window.ms_globals.React, te = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, se = window.ms_globals.React.useEffect;
function I() {
}
function re(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
function oe(n, ...e) {
  if (n == null) {
    for (const t of e)
      t(void 0);
    return I;
  }
  const s = n.subscribe(...e);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function b(n) {
  let e;
  return oe(n, (s) => e = s)(), e;
}
const y = [];
function g(n, e = I) {
  let s;
  const t = /* @__PURE__ */ new Set();
  function o(i) {
    if (re(n, i) && (n = i, s)) {
      const u = !y.length;
      for (const a of t)
        a[1](), y.push(a, n);
      if (u) {
        for (let a = 0; a < y.length; a += 2)
          y[a][0](y[a + 1]);
        y.length = 0;
      }
    }
  }
  function r(i) {
    o(i(n));
  }
  function l(i, u = I) {
    const a = [i, u];
    return t.add(a), t.size === 1 && (s = e(o, r) || I), i(n), () => {
      t.delete(a), t.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: o,
    update: r,
    subscribe: l
  };
}
const {
  getContext: W,
  setContext: F
} = window.__gradio__svelte__internal, le = "$$ms-gr-antd-slots-key";
function ie() {
  const n = g({});
  return F(le, n);
}
const ce = "$$ms-gr-antd-context-key";
function ue(n) {
  var i;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = G(), s = de({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  e && e.subscribe((u) => {
    s.slotKey.set(u);
  }), fe();
  const t = W(ce), o = ((i = b(t)) == null ? void 0 : i.as_item) || n.as_item, r = t ? o ? b(t)[o] : b(t) : {}, l = g({
    ...n,
    ...r
  });
  return t ? (t.subscribe((u) => {
    const {
      as_item: a
    } = b(l);
    a && (u = u[a]), l.update((f) => ({
      ...f,
      ...u
    }));
  }), [l, (u) => {
    const a = u.as_item ? b(t)[u.as_item] : b(t);
    return l.set({
      ...u,
      ...a
    });
  }]) : [l, (u) => {
    l.set(u);
  }];
}
const D = "$$ms-gr-antd-slot-key";
function fe() {
  F(D, g(void 0));
}
function G() {
  return W(D);
}
const ae = "$$ms-gr-antd-component-slot-context-key";
function de({
  slot: n,
  index: e,
  subIndex: s
}) {
  return F(ae, {
    slotKey: g(n),
    slotIndex: g(e),
    subSlotIndex: g(s)
  });
}
function A(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function _e(n) {
  return n && n.__esModule && Object.prototype.hasOwnProperty.call(n, "default") ? n.default : n;
}
var H = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var me = M, ge = Symbol.for("react.element"), he = Symbol.for("react.fragment"), be = Object.prototype.hasOwnProperty, ye = me.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, pe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, e, s) {
  var t, o = {}, r = null, l = null;
  s !== void 0 && (r = "" + s), e.key !== void 0 && (r = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (t in e) be.call(e, t) && !pe.hasOwnProperty(t) && (o[t] = e[t]);
  if (n && n.defaultProps) for (t in e = n.defaultProps, e) o[t] === void 0 && (o[t] = e[t]);
  return {
    $$typeof: ge,
    type: n,
    key: r,
    ref: l,
    props: o,
    _owner: ye.current
  };
}
R.Fragment = he;
R.jsx = U;
R.jsxs = U;
H.exports = R;
var k = H.exports;
const we = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(n) {
  return n ? Object.keys(n).reduce((e, s) => {
    const t = n[s];
    return typeof t == "number" && !we.includes(s) ? e[s] = t + "px" : e[s] = t, e;
  }, {}) : {};
}
function V(n) {
  const e = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((t) => {
    n.getEventListeners(t).forEach(({
      listener: r,
      type: l,
      useCapture: i
    }) => {
      e.addEventListener(l, r, i);
    });
  });
  const s = Array.from(n.children);
  for (let t = 0; t < s.length; t++) {
    const o = s[t], r = V(o);
    e.replaceChild(r, e.children[t]);
  }
  return e;
}
function Se(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const j = te(({
  slot: n,
  clone: e,
  className: s,
  style: t
}, o) => {
  const r = ne();
  return se(() => {
    var a;
    if (!r.current || !n)
      return;
    let l = n;
    function i() {
      let f = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (f = l.children[0], f.tagName.toLowerCase() === "react-portal-target" && f.children[0] && (f = f.children[0])), Se(o, f), s && f.classList.add(...s.split(" ")), t) {
        const d = xe(t);
        Object.keys(d).forEach((_) => {
          f.style[_] = d[_];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let f = function() {
        var d;
        l = V(n), l.style.display = "contents", i(), (d = r.current) == null || d.appendChild(l);
      };
      f(), u = new window.MutationObserver(() => {
        var d, _;
        (d = r.current) != null && d.contains(l) && ((_ = r.current) == null || _.removeChild(l)), f();
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      l.style.display = "contents", i(), (a = r.current) == null || a.appendChild(l);
    return () => {
      var f, d;
      l.style.display = "", (f = r.current) != null && f.contains(l) && ((d = r.current) == null || d.removeChild(l)), u == null || u.disconnect();
    };
  }, [n, e, s, t, o]), M.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  });
});
function B(n, e) {
  return n.filter(Boolean).map((s) => {
    if (typeof s != "object")
      return s;
    const t = {
      ...s.props
    };
    let o = t;
    Object.keys(s.slots).forEach((l) => {
      if (!s.slots[l] || !(s.slots[l] instanceof Element) && !s.slots[l].el)
        return;
      const i = l.split(".");
      i.forEach((_, h) => {
        o[_] || (o[_] = {}), h !== i.length - 1 && (o = t[_]);
      });
      const u = s.slots[l];
      let a, f, d = !1;
      u instanceof Element ? a = u : (a = u.el, f = u.callback, d = u.clone || !1), o[i[i.length - 1]] = a ? f ? (..._) => (f(i[i.length - 1], _), /* @__PURE__ */ k.jsx(j, {
        slot: a,
        clone: d || (e == null ? void 0 : e.clone)
      })) : /* @__PURE__ */ k.jsx(j, {
        slot: a,
        clone: d || (e == null ? void 0 : e.clone)
      }) : o[i[i.length - 1]], o = t;
    });
    const r = "children";
    return s[r] && (t[r] = B(s[r], e)), t;
  });
}
function Ce(n, e) {
  return n ? /* @__PURE__ */ k.jsx(j, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
var J = {
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
      for (var r = "", l = 0; l < arguments.length; l++) {
        var i = arguments[l];
        i && (r = o(r, t(i)));
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
      var l = "";
      for (var i in r)
        e.call(r, i) && r[i] && (l = o(l, i));
      return l;
    }
    function o(r, l) {
      return l ? r ? r + " " + l : r + l : r;
    }
    n.exports ? (s.default = s, n.exports = s) : window.classNames = s;
  })();
})(J);
var Ee = J.exports;
const ve = /* @__PURE__ */ _e(Ee), {
  getContext: Ie,
  setContext: Oe
} = window.__gradio__svelte__internal;
function Y(n) {
  const e = `$$ms-gr-antd-${n}-context-key`;
  function s(o = ["default"]) {
    const r = o.reduce((l, i) => (l[i] = g([]), l), {});
    return Oe(e, {
      itemsMap: r,
      allowedSlots: o
    }), r;
  }
  function t() {
    const {
      itemsMap: o,
      allowedSlots: r
    } = Ie(e);
    return function(l, i, u) {
      o && (l ? o[l].update((a) => {
        const f = [...a];
        return r.includes(l) ? f[i] = u : f[i] = void 0, f;
      }) : r.includes("default") && o.default.update((a) => {
        const f = [...a];
        return f[i] = u, f;
      }));
    };
  }
  return {
    getItems: s,
    getSetItemFn: t
  };
}
const {
  getItems: Re,
  getSetItemFn: Ue
} = Y("table-row-selection-selection"), {
  getItems: Ve,
  getSetItemFn: ke
} = Y("table-row-selection"), {
  SvelteComponent: je,
  check_outros: Pe,
  component_subscribe: w,
  create_slot: Fe,
  detach: Ne,
  empty: Le,
  flush: m,
  get_all_dirty_from_scope: Ke,
  get_slot_changes: qe,
  group_outros: Te,
  init: Ae,
  insert: ze,
  safe_not_equal: Me,
  transition_in: O,
  transition_out: P,
  update_slot_base: We
} = window.__gradio__svelte__internal;
function z(n) {
  let e;
  const s = (
    /*#slots*/
    n[20].default
  ), t = Fe(
    s,
    n,
    /*$$scope*/
    n[19],
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
      524288) && We(
        t,
        s,
        o,
        /*$$scope*/
        o[19],
        e ? qe(
          s,
          /*$$scope*/
          o[19],
          r,
          null
        ) : Ke(
          /*$$scope*/
          o[19]
        ),
        null
      );
    },
    i(o) {
      e || (O(t, o), e = !0);
    },
    o(o) {
      P(t, o), e = !1;
    },
    d(o) {
      t && t.d(o);
    }
  };
}
function De(n) {
  let e, s, t = (
    /*$mergedProps*/
    n[0].visible && z(n)
  );
  return {
    c() {
      t && t.c(), e = Le();
    },
    m(o, r) {
      t && t.m(o, r), ze(o, e, r), s = !0;
    },
    p(o, [r]) {
      /*$mergedProps*/
      o[0].visible ? t ? (t.p(o, r), r & /*$mergedProps*/
      1 && O(t, 1)) : (t = z(o), t.c(), O(t, 1), t.m(e.parentNode, e)) : t && (Te(), P(t, 1, 1, () => {
        t = null;
      }), Pe());
    },
    i(o) {
      s || (O(t), s = !0);
    },
    o(o) {
      P(t), s = !1;
    },
    d(o) {
      o && Ne(e), t && t.d(o);
    }
  };
}
function Ge(n, e, s) {
  let t, o, r, l, i, {
    $$slots: u = {},
    $$scope: a
  } = e, {
    gradio: f
  } = e, {
    props: d = {}
  } = e;
  const _ = g(d);
  w(n, _, (c) => s(18, i = c));
  let {
    _internal: h = {}
  } = e, {
    as_item: x
  } = e, {
    value: p
  } = e, {
    visible: S = !0
  } = e, {
    elem_id: C = ""
  } = e, {
    elem_classes: E = []
  } = e, {
    elem_style: v = {}
  } = e;
  const N = G();
  w(n, N, (c) => s(17, l = c));
  const [L, Q] = ue({
    gradio: f,
    props: i,
    _internal: h,
    visible: S,
    elem_id: C,
    elem_classes: E,
    elem_style: v,
    as_item: x,
    value: p
  });
  w(n, L, (c) => s(0, t = c));
  const K = ie();
  w(n, K, (c) => s(15, o = c));
  const {
    selections: q
  } = Re(["selections"]);
  w(n, q, (c) => s(16, r = c));
  const X = ke();
  return n.$$set = (c) => {
    "gradio" in c && s(7, f = c.gradio), "props" in c && s(8, d = c.props), "_internal" in c && s(9, h = c._internal), "as_item" in c && s(10, x = c.as_item), "value" in c && s(6, p = c.value), "visible" in c && s(11, S = c.visible), "elem_id" in c && s(12, C = c.elem_id), "elem_classes" in c && s(13, E = c.elem_classes), "elem_style" in c && s(14, v = c.elem_style), "$$scope" in c && s(19, a = c.$$scope);
  }, n.$$.update = () => {
    if (n.$$.dirty & /*props*/
    256 && _.update((c) => ({
      ...c,
      ...d
    })), n.$$.dirty & /*$mergedProps, $slotKey, $selectionsItems, $slots*/
    229377) {
      const c = ee(t);
      X(l, t._internal.index || 0, {
        props: {
          style: t.elem_style,
          className: ve(t.elem_classes, "ms-gr-antd-table-row-selection"),
          id: t.elem_id,
          selectedRowKeys: t.value,
          selections: t.props.selections || B(r),
          ...t.props,
          ...c,
          onChange: (Z, ...$) => {
            var T;
            s(6, p = Z), (T = c == null ? void 0 : c.onChange) == null || T.call(c, ...$);
          },
          onCell: A(t.props.onCell),
          getCheckboxProps: A(t.props.getCheckboxProps),
          columnTitle: Ce(o.columnTitle) || t.props.columnTitle
        },
        slots: {}
      });
    }
    n.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    294592 && Q({
      gradio: f,
      props: i,
      _internal: h,
      visible: S,
      elem_id: C,
      elem_classes: E,
      elem_style: v,
      as_item: x,
      value: p
    });
  }, [t, _, N, L, K, q, p, f, d, h, x, S, C, E, v, o, r, l, i, a, u];
}
class Be extends je {
  constructor(e) {
    super(), Ae(this, e, Ge, De, Me, {
      gradio: 7,
      props: 8,
      _internal: 9,
      as_item: 10,
      value: 6,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), m();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), m();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), m();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), m();
  }
  get value() {
    return this.$$.ctx[6];
  }
  set value(e) {
    this.$$set({
      value: e
    }), m();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), m();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), m();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), m();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), m();
  }
}
export {
  Be as default
};
