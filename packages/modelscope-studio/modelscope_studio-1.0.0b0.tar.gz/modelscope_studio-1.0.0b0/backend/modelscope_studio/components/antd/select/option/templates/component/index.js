function G(e) {
  const {
    gradio: t,
    _internal: s,
    ...n
  } = e;
  return Object.keys(s).reduce((i, l) => {
    const o = l.match(/bind_(.+)_event/);
    if (o) {
      const u = o[1], c = u.split("_"), a = (...m) => {
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
        return t.dispatch(u.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: b,
          component: n
        });
      };
      if (c.length > 1) {
        let m = {
          ...n.props[c[0]] || {}
        };
        i[c[0]] = m;
        for (let f = 1; f < c.length - 1; f++) {
          const h = {
            ...n.props[c[f]] || {}
          };
          m[c[f]] = h, m = h;
        }
        const b = c[c.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = a, i;
      }
      const _ = c[0];
      i[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = a;
    }
    return i;
  }, {});
}
function N() {
}
function H(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function J(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return N;
  }
  const s = e.subscribe(...t);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function g(e) {
  let t;
  return J(e, (s) => t = s)(), t;
}
const x = [];
function y(e, t = N) {
  let s;
  const n = /* @__PURE__ */ new Set();
  function i(u) {
    if (H(e, u) && (e = u, s)) {
      const c = !x.length;
      for (const a of n)
        a[1](), x.push(a, e);
      if (c) {
        for (let a = 0; a < x.length; a += 2)
          x[a][0](x[a + 1]);
        x.length = 0;
      }
    }
  }
  function l(u) {
    i(u(e));
  }
  function o(u, c = N) {
    const a = [u, c];
    return n.add(a), n.size === 1 && (s = t(i, l) || N), u(e), () => {
      n.delete(a), n.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: i,
    update: l,
    subscribe: o
  };
}
const {
  getContext: X,
  setContext: A
} = window.__gradio__svelte__internal, Q = "$$ms-gr-antd-slots-key";
function T() {
  const e = y({});
  return A(Q, e);
}
const W = "$$ms-gr-antd-context-key";
function $(e) {
  var u;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = D(), s = nt({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((c) => {
    s.slotKey.set(c);
  }), tt();
  const n = X(W), i = ((u = g(n)) == null ? void 0 : u.as_item) || e.as_item, l = n ? i ? g(n)[i] : g(n) : {}, o = y({
    ...e,
    ...l
  });
  return n ? (n.subscribe((c) => {
    const {
      as_item: a
    } = g(o);
    a && (c = c[a]), o.update((_) => ({
      ..._,
      ...c
    }));
  }), [o, (c) => {
    const a = c.as_item ? g(n)[c.as_item] : g(n);
    return o.set({
      ...c,
      ...a
    });
  }]) : [o, (c) => {
    o.set(c);
  }];
}
const Y = "$$ms-gr-antd-slot-key";
function tt() {
  A(Y, y(void 0));
}
function D() {
  return X(Y);
}
const et = "$$ms-gr-antd-component-slot-context-key";
function nt({
  slot: e,
  index: t,
  subIndex: s
}) {
  return A(et, {
    slotKey: y(e),
    slotIndex: y(t),
    subSlotIndex: y(s)
  });
}
function st(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var L = {
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
      for (var l = "", o = 0; o < arguments.length; o++) {
        var u = arguments[o];
        u && (l = i(l, n(u)));
      }
      return l;
    }
    function n(l) {
      if (typeof l == "string" || typeof l == "number")
        return l;
      if (typeof l != "object")
        return "";
      if (Array.isArray(l))
        return s.apply(null, l);
      if (l.toString !== Object.prototype.toString && !l.toString.toString().includes("[native code]"))
        return l.toString();
      var o = "";
      for (var u in l)
        t.call(l, u) && l[u] && (o = i(o, u));
      return o;
    }
    function i(l, o) {
      return o ? l ? l + " " + o : l + o : l;
    }
    e.exports ? (s.default = s, e.exports = s) : window.classNames = s;
  })();
})(L);
var it = L.exports;
const lt = /* @__PURE__ */ st(it), {
  getContext: ot,
  setContext: rt
} = window.__gradio__svelte__internal;
function ct(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function s(i = ["default"]) {
    const l = i.reduce((o, u) => (o[u] = y([]), o), {});
    return rt(t, {
      itemsMap: l,
      allowedSlots: i
    }), l;
  }
  function n() {
    const {
      itemsMap: i,
      allowedSlots: l
    } = ot(t);
    return function(o, u, c) {
      i && (o ? i[o].update((a) => {
        const _ = [...a];
        return l.includes(o) ? _[u] = c : _[u] = void 0, _;
      }) : l.includes("default") && i.default.update((a) => {
        const _ = [...a];
        return _[u] = c, _;
      }));
    };
  }
  return {
    getItems: s,
    getSetItemFn: n
  };
}
const {
  getItems: ut,
  getSetItemFn: ft
} = ct("select"), {
  SvelteComponent: at,
  check_outros: _t,
  component_subscribe: p,
  create_slot: dt,
  detach: mt,
  empty: bt,
  flush: d,
  get_all_dirty_from_scope: yt,
  get_slot_changes: ht,
  group_outros: gt,
  init: xt,
  insert: pt,
  safe_not_equal: Ct,
  transition_in: O,
  transition_out: q,
  update_slot_base: Kt
} = window.__gradio__svelte__internal;
function U(e) {
  let t;
  const s = (
    /*#slots*/
    e[26].default
  ), n = dt(
    s,
    e,
    /*$$scope*/
    e[25],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, l) {
      n && n.m(i, l), t = !0;
    },
    p(i, l) {
      n && n.p && (!t || l & /*$$scope*/
      33554432) && Kt(
        n,
        s,
        i,
        /*$$scope*/
        i[25],
        t ? ht(
          s,
          /*$$scope*/
          i[25],
          l,
          null
        ) : yt(
          /*$$scope*/
          i[25]
        ),
        null
      );
    },
    i(i) {
      t || (O(n, i), t = !0);
    },
    o(i) {
      q(n, i), t = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function St(e) {
  let t, s, n = (
    /*$mergedProps*/
    e[0].visible && U(e)
  );
  return {
    c() {
      n && n.c(), t = bt();
    },
    m(i, l) {
      n && n.m(i, l), pt(i, t, l), s = !0;
    },
    p(i, [l]) {
      /*$mergedProps*/
      i[0].visible ? n ? (n.p(i, l), l & /*$mergedProps*/
      1 && O(n, 1)) : (n = U(i), n.c(), O(n, 1), n.m(t.parentNode, t)) : n && (gt(), q(n, 1, 1, () => {
        n = null;
      }), _t());
    },
    i(i) {
      s || (O(n), s = !0);
    },
    o(i) {
      q(n), s = !1;
    },
    d(i) {
      i && mt(t), n && n.d(i);
    }
  };
}
function kt(e, t, s) {
  let n, i, l, o, u, c, {
    $$slots: a = {},
    $$scope: _
  } = t, {
    gradio: m
  } = t, {
    props: b = {}
  } = t;
  const f = y(b);
  p(e, f, (r) => s(24, c = r));
  let {
    _internal: h = {}
  } = t, {
    value: C
  } = t, {
    label: K
  } = t, {
    disabled: S
  } = t, {
    title: k
  } = t, {
    key: w
  } = t, {
    as_item: I
  } = t, {
    visible: v = !0
  } = t, {
    elem_id: j = ""
  } = t, {
    elem_classes: P = []
  } = t, {
    elem_style: E = {}
  } = t;
  const F = D();
  p(e, F, (r) => s(23, u = r));
  const [M, Z] = $({
    gradio: m,
    props: c,
    _internal: h,
    visible: v,
    elem_id: j,
    elem_classes: P,
    elem_style: E,
    as_item: I,
    value: C,
    label: K,
    disabled: S,
    title: k,
    key: w
  });
  p(e, M, (r) => s(0, o = r));
  const V = T();
  p(e, V, (r) => s(22, l = r));
  const B = ft(), {
    default: z,
    options: R
  } = ut(["default", "options"]);
  return p(e, z, (r) => s(20, n = r)), p(e, R, (r) => s(21, i = r)), e.$$set = (r) => {
    "gradio" in r && s(7, m = r.gradio), "props" in r && s(8, b = r.props), "_internal" in r && s(9, h = r._internal), "value" in r && s(10, C = r.value), "label" in r && s(11, K = r.label), "disabled" in r && s(12, S = r.disabled), "title" in r && s(13, k = r.title), "key" in r && s(14, w = r.key), "as_item" in r && s(15, I = r.as_item), "visible" in r && s(16, v = r.visible), "elem_id" in r && s(17, j = r.elem_id), "elem_classes" in r && s(18, P = r.elem_classes), "elem_style" in r && s(19, E = r.elem_style), "$$scope" in r && s(25, _ = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    256 && f.update((r) => ({
      ...r,
      ...b
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value, label, disabled, title, key*/
    17825408 && Z({
      gradio: m,
      props: c,
      _internal: h,
      visible: v,
      elem_id: j,
      elem_classes: P,
      elem_style: E,
      as_item: I,
      value: C,
      label: K,
      disabled: S,
      title: k,
      key: w
    }), e.$$.dirty & /*$slotKey, $mergedProps, $slots, $options, $items*/
    15728641 && B(u, o._internal.index || 0, {
      props: {
        style: o.elem_style,
        className: lt(o.elem_classes, "ms-gr-antd-select-option"),
        id: o.elem_id,
        value: o.value,
        label: o.label,
        disabled: o.disabled,
        title: o.title,
        key: o.key,
        ...o.props,
        ...G(o)
      },
      slots: l,
      options: i.length > 0 ? i : n.length > 0 ? n : void 0
    });
  }, [o, f, F, M, V, z, R, m, b, h, C, K, S, k, w, I, v, j, P, E, n, i, l, u, c, _, a];
}
class wt extends at {
  constructor(t) {
    super(), xt(this, t, kt, St, Ct, {
      gradio: 7,
      props: 8,
      _internal: 9,
      value: 10,
      label: 11,
      disabled: 12,
      title: 13,
      key: 14,
      as_item: 15,
      visible: 16,
      elem_id: 17,
      elem_classes: 18,
      elem_style: 19
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
  get disabled() {
    return this.$$.ctx[12];
  }
  set disabled(t) {
    this.$$set({
      disabled: t
    }), d();
  }
  get title() {
    return this.$$.ctx[13];
  }
  set title(t) {
    this.$$set({
      title: t
    }), d();
  }
  get key() {
    return this.$$.ctx[14];
  }
  set key(t) {
    this.$$set({
      key: t
    }), d();
  }
  get as_item() {
    return this.$$.ctx[15];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), d();
  }
  get visible() {
    return this.$$.ctx[16];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[17];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[18];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[19];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), d();
  }
}
export {
  wt as default
};
