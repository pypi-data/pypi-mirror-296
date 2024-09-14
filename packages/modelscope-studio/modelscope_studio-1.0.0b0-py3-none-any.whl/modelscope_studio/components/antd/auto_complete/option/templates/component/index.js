function L(e) {
  const {
    gradio: t,
    _internal: s,
    ...n
  } = e;
  return Object.keys(s).reduce((i, o) => {
    const l = o.match(/bind_(.+)_event/);
    if (l) {
      const c = l[1], u = c.split("_"), a = (...m) => {
        const b = m.map((f) => m && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
          type: f.type,
          detail: f.detail,
          timestamp: f.timeStamp,
          clientX: f.clientX,
          clientY: f.clientY,
          targetId: f.target.id,
          targetClassName: f.target.className,
          altKey: f.altKey,
          ctrlKey: f.ctrlKey,
          shiftKey: f.shiftKey,
          metaKey: f.metaKey
        } : f);
        return t.dispatch(c.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: b,
          component: n
        });
      };
      if (u.length > 1) {
        let m = {
          ...n.props[u[0]] || {}
        };
        i[u[0]] = m;
        for (let f = 1; f < u.length - 1; f++) {
          const h = {
            ...n.props[u[f]] || {}
          };
          m[u[f]] = h, m = h;
        }
        const b = u[u.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = a, i;
      }
      const _ = u[0];
      i[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = a;
    }
    return i;
  }, {});
}
function j() {
}
function Z(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function B(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return j;
  }
  const s = e.subscribe(...t);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function g(e) {
  let t;
  return B(e, (s) => t = s)(), t;
}
const p = [];
function y(e, t = j) {
  let s;
  const n = /* @__PURE__ */ new Set();
  function i(c) {
    if (Z(e, c) && (e = c, s)) {
      const u = !p.length;
      for (const a of n)
        a[1](), p.push(a, e);
      if (u) {
        for (let a = 0; a < p.length; a += 2)
          p[a][0](p[a + 1]);
        p.length = 0;
      }
    }
  }
  function o(c) {
    i(c(e));
  }
  function l(c, u = j) {
    const a = [c, u];
    return n.add(a), n.size === 1 && (s = t(i, o) || j), c(e), () => {
      n.delete(a), n.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: i,
    update: o,
    subscribe: l
  };
}
const {
  getContext: z,
  setContext: N
} = window.__gradio__svelte__internal, G = "$$ms-gr-antd-slots-key";
function H() {
  const e = y({});
  return N(G, e);
}
const J = "$$ms-gr-antd-context-key";
function Q(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = U(), s = $({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((u) => {
    s.slotKey.set(u);
  }), T();
  const n = z(J), i = ((c = g(n)) == null ? void 0 : c.as_item) || e.as_item, o = n ? i ? g(n)[i] : g(n) : {}, l = y({
    ...e,
    ...o
  });
  return n ? (n.subscribe((u) => {
    const {
      as_item: a
    } = g(l);
    a && (u = u[a]), l.update((_) => ({
      ..._,
      ...u
    }));
  }), [l, (u) => {
    const a = u.as_item ? g(n)[u.as_item] : g(n);
    return l.set({
      ...u,
      ...a
    });
  }]) : [l, (u) => {
    l.set(u);
  }];
}
const R = "$$ms-gr-antd-slot-key";
function T() {
  N(R, y(void 0));
}
function U() {
  return z(R);
}
const W = "$$ms-gr-antd-component-slot-context-key";
function $({
  slot: e,
  index: t,
  subIndex: s
}) {
  return N(W, {
    slotKey: y(e),
    slotIndex: y(t),
    subSlotIndex: y(s)
  });
}
function tt(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var X = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function s() {
      for (var o = "", l = 0; l < arguments.length; l++) {
        var c = arguments[l];
        c && (o = i(o, n(c)));
      }
      return o;
    }
    function n(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return s.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var l = "";
      for (var c in o)
        t.call(o, c) && o[c] && (l = i(l, c));
      return l;
    }
    function i(o, l) {
      return l ? o ? o + " " + l : o + l : o;
    }
    e.exports ? (s.default = s, e.exports = s) : window.classNames = s;
  })();
})(X);
var et = X.exports;
const nt = /* @__PURE__ */ tt(et), {
  getContext: st,
  setContext: it
} = window.__gradio__svelte__internal;
function ot(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function s(i = ["default"]) {
    const o = i.reduce((l, c) => (l[c] = y([]), l), {});
    return it(t, {
      itemsMap: o,
      allowedSlots: i
    }), o;
  }
  function n() {
    const {
      itemsMap: i,
      allowedSlots: o
    } = st(t);
    return function(l, c, u) {
      i && (l ? i[l].update((a) => {
        const _ = [...a];
        return o.includes(l) ? _[c] = u : _[c] = void 0, _;
      }) : o.includes("default") && i.default.update((a) => {
        const _ = [...a];
        return _[c] = u, _;
      }));
    };
  }
  return {
    getItems: s,
    getSetItemFn: n
  };
}
const {
  getItems: lt,
  getSetItemFn: rt
} = ot("auto-complete"), {
  SvelteComponent: ut,
  check_outros: ct,
  component_subscribe: x,
  create_slot: ft,
  detach: at,
  empty: _t,
  flush: d,
  get_all_dirty_from_scope: mt,
  get_slot_changes: dt,
  group_outros: bt,
  init: yt,
  insert: ht,
  safe_not_equal: gt,
  transition_in: P,
  transition_out: E,
  update_slot_base: pt
} = window.__gradio__svelte__internal;
function V(e) {
  let t;
  const s = (
    /*#slots*/
    e[23].default
  ), n = ft(
    s,
    e,
    /*$$scope*/
    e[22],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, o) {
      n && n.m(i, o), t = !0;
    },
    p(i, o) {
      n && n.p && (!t || o & /*$$scope*/
      4194304) && pt(
        n,
        s,
        i,
        /*$$scope*/
        i[22],
        t ? dt(
          s,
          /*$$scope*/
          i[22],
          o,
          null
        ) : mt(
          /*$$scope*/
          i[22]
        ),
        null
      );
    },
    i(i) {
      t || (P(n, i), t = !0);
    },
    o(i) {
      E(n, i), t = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function xt(e) {
  let t, s, n = (
    /*$mergedProps*/
    e[0].visible && V(e)
  );
  return {
    c() {
      n && n.c(), t = _t();
    },
    m(i, o) {
      n && n.m(i, o), ht(i, t, o), s = !0;
    },
    p(i, [o]) {
      /*$mergedProps*/
      i[0].visible ? n ? (n.p(i, o), o & /*$mergedProps*/
      1 && P(n, 1)) : (n = V(i), n.c(), P(n, 1), n.m(t.parentNode, t)) : n && (bt(), E(n, 1, 1, () => {
        n = null;
      }), ct());
    },
    i(i) {
      s || (P(n), s = !0);
    },
    o(i) {
      E(n), s = !1;
    },
    d(i) {
      i && at(t), n && n.d(i);
    }
  };
}
function Ct(e, t, s) {
  let n, i, o, l, c, u, {
    $$slots: a = {},
    $$scope: _
  } = t, {
    gradio: m
  } = t, {
    props: b = {}
  } = t;
  const f = y(b);
  x(e, f, (r) => s(21, u = r));
  let {
    _internal: h = {}
  } = t, {
    value: C
  } = t, {
    label: K
  } = t, {
    as_item: S
  } = t, {
    visible: w = !0
  } = t, {
    elem_id: v = ""
  } = t, {
    elem_classes: I = []
  } = t, {
    elem_style: k = {}
  } = t;
  const O = U();
  x(e, O, (r) => s(20, c = r));
  const [q, Y] = Q({
    gradio: m,
    props: u,
    _internal: h,
    visible: w,
    elem_id: v,
    elem_classes: I,
    elem_style: k,
    as_item: S,
    value: C,
    label: K
  });
  x(e, q, (r) => s(0, l = r));
  const A = H();
  x(e, A, (r) => s(19, o = r));
  const D = rt(), {
    default: F,
    options: M
  } = lt(["default", "options"]);
  return x(e, F, (r) => s(17, n = r)), x(e, M, (r) => s(18, i = r)), e.$$set = (r) => {
    "gradio" in r && s(7, m = r.gradio), "props" in r && s(8, b = r.props), "_internal" in r && s(9, h = r._internal), "value" in r && s(10, C = r.value), "label" in r && s(11, K = r.label), "as_item" in r && s(12, S = r.as_item), "visible" in r && s(13, w = r.visible), "elem_id" in r && s(14, v = r.elem_id), "elem_classes" in r && s(15, I = r.elem_classes), "elem_style" in r && s(16, k = r.elem_style), "$$scope" in r && s(22, _ = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    256 && f.update((r) => ({
      ...r,
      ...b
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value, label*/
    2227840 && Y({
      gradio: m,
      props: u,
      _internal: h,
      visible: w,
      elem_id: v,
      elem_classes: I,
      elem_style: k,
      as_item: S,
      value: C,
      label: K
    }), e.$$.dirty & /*$slotKey, $mergedProps, $slots, $options, $items*/
    1966081 && D(c, l._internal.index || 0, {
      props: {
        style: l.elem_style,
        className: nt(l.elem_classes, "ms-gr-antd-auto-complete-option"),
        id: l.elem_id,
        value: l.value,
        label: l.label,
        ...l.props,
        ...L(l)
      },
      slots: o,
      options: i.length > 0 ? i : n.length > 0 ? n : void 0
    });
  }, [l, f, O, q, A, F, M, m, b, h, C, K, S, w, v, I, k, n, i, o, c, u, _, a];
}
class Kt extends ut {
  constructor(t) {
    super(), yt(this, t, Ct, xt, gt, {
      gradio: 7,
      props: 8,
      _internal: 9,
      value: 10,
      label: 11,
      as_item: 12,
      visible: 13,
      elem_id: 14,
      elem_classes: 15,
      elem_style: 16
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), d();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), d();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), d();
  }
  get value() {
    return this.$$.ctx[10];
  }
  set value(t) {
    this.$$set({
      value: t
    }), d();
  }
  get label() {
    return this.$$.ctx[11];
  }
  set label(t) {
    this.$$set({
      label: t
    }), d();
  }
  get as_item() {
    return this.$$.ctx[12];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), d();
  }
  get visible() {
    return this.$$.ctx[13];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[14];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[15];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[16];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), d();
  }
}
export {
  Kt as default
};
