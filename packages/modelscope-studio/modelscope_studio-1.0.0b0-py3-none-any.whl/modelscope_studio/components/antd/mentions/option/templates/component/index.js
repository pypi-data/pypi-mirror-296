function B(t) {
  const {
    gradio: e,
    _internal: s,
    ...n
  } = t;
  return Object.keys(s).reduce((i, l) => {
    const o = l.match(/bind_(.+)_event/);
    if (o) {
      const c = o[1], u = c.split("_"), a = (...d) => {
        const b = d.map((f) => d && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
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
        return e.dispatch(c.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: b,
          component: n
        });
      };
      if (u.length > 1) {
        let d = {
          ...n.props[u[0]] || {}
        };
        i[u[0]] = d;
        for (let f = 1; f < u.length - 1; f++) {
          const h = {
            ...n.props[u[f]] || {}
          };
          d[u[f]] = h, d = h;
        }
        const b = u[u.length - 1];
        return d[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = a, i;
      }
      const _ = u[0];
      i[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = a;
    }
    return i;
  }, {});
}
function E() {
}
function G(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function H(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return E;
  }
  const s = t.subscribe(...e);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function g(t) {
  let e;
  return H(t, (s) => e = s)(), e;
}
const x = [];
function y(t, e = E) {
  let s;
  const n = /* @__PURE__ */ new Set();
  function i(c) {
    if (G(t, c) && (t = c, s)) {
      const u = !x.length;
      for (const a of n)
        a[1](), x.push(a, t);
      if (u) {
        for (let a = 0; a < x.length; a += 2)
          x[a][0](x[a + 1]);
        x.length = 0;
      }
    }
  }
  function l(c) {
    i(c(t));
  }
  function o(c, u = E) {
    const a = [c, u];
    return n.add(a), n.size === 1 && (s = e(i, l) || E), c(t), () => {
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
  getContext: U,
  setContext: q
} = window.__gradio__svelte__internal, J = "$$ms-gr-antd-slots-key";
function Q() {
  const t = y({});
  return q(J, t);
}
const T = "$$ms-gr-antd-context-key";
function W(t) {
  var c;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = Y(), s = te({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((u) => {
    s.slotKey.set(u);
  }), $();
  const n = U(T), i = ((c = g(n)) == null ? void 0 : c.as_item) || t.as_item, l = n ? i ? g(n)[i] : g(n) : {}, o = y({
    ...t,
    ...l
  });
  return n ? (n.subscribe((u) => {
    const {
      as_item: a
    } = g(o);
    a && (u = u[a]), o.update((_) => ({
      ..._,
      ...u
    }));
  }), [o, (u) => {
    const a = u.as_item ? g(n)[u.as_item] : g(n);
    return o.set({
      ...u,
      ...a
    });
  }]) : [o, (u) => {
    o.set(u);
  }];
}
const X = "$$ms-gr-antd-slot-key";
function $() {
  q(X, y(void 0));
}
function Y() {
  return U(X);
}
const ee = "$$ms-gr-antd-component-slot-context-key";
function te({
  slot: t,
  index: e,
  subIndex: s
}) {
  return q(ee, {
    slotKey: y(t),
    slotIndex: y(e),
    subSlotIndex: y(s)
  });
}
function ne(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var D = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(t) {
  (function() {
    var e = {}.hasOwnProperty;
    function s() {
      for (var l = "", o = 0; o < arguments.length; o++) {
        var c = arguments[o];
        c && (l = i(l, n(c)));
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
      for (var c in l)
        e.call(l, c) && l[c] && (o = i(o, c));
      return o;
    }
    function i(l, o) {
      return o ? l ? l + " " + o : l + o : l;
    }
    t.exports ? (s.default = s, t.exports = s) : window.classNames = s;
  })();
})(D);
var se = D.exports;
const ie = /* @__PURE__ */ ne(se), {
  getContext: le,
  setContext: oe
} = window.__gradio__svelte__internal;
function re(t) {
  const e = `$$ms-gr-antd-${t}-context-key`;
  function s(i = ["default"]) {
    const l = i.reduce((o, c) => (o[c] = y([]), o), {});
    return oe(e, {
      itemsMap: l,
      allowedSlots: i
    }), l;
  }
  function n() {
    const {
      itemsMap: i,
      allowedSlots: l
    } = le(e);
    return function(o, c, u) {
      i && (o ? i[o].update((a) => {
        const _ = [...a];
        return l.includes(o) ? _[c] = u : _[c] = void 0, _;
      }) : l.includes("default") && i.default.update((a) => {
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
  getItems: ue,
  getSetItemFn: ce
} = re("mentions"), {
  SvelteComponent: fe,
  check_outros: ae,
  component_subscribe: p,
  create_slot: _e,
  detach: de,
  empty: me,
  flush: m,
  get_all_dirty_from_scope: be,
  get_slot_changes: ye,
  group_outros: he,
  init: ge,
  insert: xe,
  safe_not_equal: pe,
  transition_in: N,
  transition_out: O,
  update_slot_base: Ce
} = window.__gradio__svelte__internal;
function R(t) {
  let e;
  const s = (
    /*#slots*/
    t[25].default
  ), n = _e(
    s,
    t,
    /*$$scope*/
    t[24],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, l) {
      n && n.m(i, l), e = !0;
    },
    p(i, l) {
      n && n.p && (!e || l & /*$$scope*/
      16777216) && Ce(
        n,
        s,
        i,
        /*$$scope*/
        i[24],
        e ? ye(
          s,
          /*$$scope*/
          i[24],
          l,
          null
        ) : be(
          /*$$scope*/
          i[24]
        ),
        null
      );
    },
    i(i) {
      e || (N(n, i), e = !0);
    },
    o(i) {
      O(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function Ke(t) {
  let e, s, n = (
    /*$mergedProps*/
    t[0].visible && R(t)
  );
  return {
    c() {
      n && n.c(), e = me();
    },
    m(i, l) {
      n && n.m(i, l), xe(i, e, l), s = !0;
    },
    p(i, [l]) {
      /*$mergedProps*/
      i[0].visible ? n ? (n.p(i, l), l & /*$mergedProps*/
      1 && N(n, 1)) : (n = R(i), n.c(), N(n, 1), n.m(e.parentNode, e)) : n && (he(), O(n, 1, 1, () => {
        n = null;
      }), ae());
    },
    i(i) {
      s || (N(n), s = !0);
    },
    o(i) {
      O(n), s = !1;
    },
    d(i) {
      i && de(e), n && n.d(i);
    }
  };
}
function Se(t, e, s) {
  let n, i, l, o, c, u, {
    $$slots: a = {},
    $$scope: _
  } = e, {
    gradio: d
  } = e, {
    props: b = {}
  } = e;
  const f = y(b);
  p(t, f, (r) => s(23, u = r));
  let {
    _internal: h = {}
  } = e, {
    value: C
  } = e, {
    label: K
  } = e, {
    disabled: S
  } = e, {
    key: k
  } = e, {
    as_item: w
  } = e, {
    visible: v = !0
  } = e, {
    elem_id: I = ""
  } = e, {
    elem_classes: j = []
  } = e, {
    elem_style: P = {}
  } = e;
  const A = Y();
  p(t, A, (r) => s(22, c = r));
  const [F, L] = W({
    gradio: d,
    props: u,
    _internal: h,
    visible: v,
    elem_id: I,
    elem_classes: j,
    elem_style: P,
    as_item: w,
    value: C,
    disabled: S,
    key: k,
    label: K
  });
  p(t, F, (r) => s(0, o = r));
  const M = Q();
  p(t, M, (r) => s(21, l = r));
  const Z = ce(), {
    default: V,
    options: z
  } = ue(["default", "options"]);
  return p(t, V, (r) => s(19, n = r)), p(t, z, (r) => s(20, i = r)), t.$$set = (r) => {
    "gradio" in r && s(7, d = r.gradio), "props" in r && s(8, b = r.props), "_internal" in r && s(9, h = r._internal), "value" in r && s(10, C = r.value), "label" in r && s(11, K = r.label), "disabled" in r && s(12, S = r.disabled), "key" in r && s(13, k = r.key), "as_item" in r && s(14, w = r.as_item), "visible" in r && s(15, v = r.visible), "elem_id" in r && s(16, I = r.elem_id), "elem_classes" in r && s(17, j = r.elem_classes), "elem_style" in r && s(18, P = r.elem_style), "$$scope" in r && s(24, _ = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    256 && f.update((r) => ({
      ...r,
      ...b
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value, disabled, key, label*/
    8912512 && L({
      gradio: d,
      props: u,
      _internal: h,
      visible: v,
      elem_id: I,
      elem_classes: j,
      elem_style: P,
      as_item: w,
      value: C,
      disabled: S,
      key: k,
      label: K
    }), t.$$.dirty & /*$slotKey, $mergedProps, $slots, $options, $items*/
    7864321 && Z(c, o._internal.index || 0, {
      props: {
        style: o.elem_style,
        className: ie(o.elem_classes, "ms-gr-antd-mentions-option"),
        id: o.elem_id,
        value: o.value,
        label: o.label,
        disabled: o.disabled,
        key: o.key,
        ...o.props,
        ...B(o)
      },
      slots: l,
      options: i.length > 0 ? i : n.length > 0 ? n : void 0
    });
  }, [o, f, A, F, M, V, z, d, b, h, C, K, S, k, w, v, I, j, P, n, i, l, c, u, _, a];
}
class ke extends fe {
  constructor(e) {
    super(), ge(this, e, Se, Ke, pe, {
      gradio: 7,
      props: 8,
      _internal: 9,
      value: 10,
      label: 11,
      disabled: 12,
      key: 13,
      as_item: 14,
      visible: 15,
      elem_id: 16,
      elem_classes: 17,
      elem_style: 18
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
  get value() {
    return this.$$.ctx[10];
  }
  set value(e) {
    this.$$set({
      value: e
    }), m();
  }
  get label() {
    return this.$$.ctx[11];
  }
  set label(e) {
    this.$$set({
      label: e
    }), m();
  }
  get disabled() {
    return this.$$.ctx[12];
  }
  set disabled(e) {
    this.$$set({
      disabled: e
    }), m();
  }
  get key() {
    return this.$$.ctx[13];
  }
  set key(e) {
    this.$$set({
      key: e
    }), m();
  }
  get as_item() {
    return this.$$.ctx[14];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), m();
  }
  get visible() {
    return this.$$.ctx[15];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), m();
  }
  get elem_id() {
    return this.$$.ctx[16];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), m();
  }
  get elem_classes() {
    return this.$$.ctx[17];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), m();
  }
  get elem_style() {
    return this.$$.ctx[18];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), m();
  }
}
export {
  ke as default
};
