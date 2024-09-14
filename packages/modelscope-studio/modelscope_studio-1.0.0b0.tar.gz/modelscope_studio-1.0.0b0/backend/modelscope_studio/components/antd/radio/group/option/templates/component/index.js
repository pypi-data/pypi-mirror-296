function D(n) {
  const {
    gradio: e,
    _internal: i,
    ...s
  } = n;
  return Object.keys(i).reduce((t, l) => {
    const o = l.match(/bind_(.+)_event/);
    if (o) {
      const c = o[1], u = c.split("_"), a = (...m) => {
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
        return e.dispatch(c.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: b,
          component: s
        });
      };
      if (u.length > 1) {
        let m = {
          ...s.props[u[0]] || {}
        };
        t[u[0]] = m;
        for (let f = 1; f < u.length - 1; f++) {
          const y = {
            ...s.props[u[f]] || {}
          };
          m[u[f]] = y, m = y;
        }
        const b = u[u.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = a, t;
      }
      const d = u[0];
      t[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = a;
    }
    return t;
  }, {});
}
function j() {
}
function L(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
function Z(n, ...e) {
  if (n == null) {
    for (const s of e)
      s(void 0);
    return j;
  }
  const i = n.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(n) {
  let e;
  return Z(n, (i) => e = i)(), e;
}
const x = [];
function h(n, e = j) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function t(c) {
    if (L(n, c) && (n = c, i)) {
      const u = !x.length;
      for (const a of s)
        a[1](), x.push(a, n);
      if (u) {
        for (let a = 0; a < x.length; a += 2)
          x[a][0](x[a + 1]);
        x.length = 0;
      }
    }
  }
  function l(c) {
    t(c(n));
  }
  function o(c, u = j) {
    const a = [c, u];
    return s.add(a), s.size === 1 && (i = e(t, l) || j), c(n), () => {
      s.delete(a), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: t,
    update: l,
    subscribe: o
  };
}
const {
  getContext: V,
  setContext: N
} = window.__gradio__svelte__internal, B = "$$ms-gr-antd-slots-key";
function G() {
  const n = h({});
  return N(B, n);
}
const H = "$$ms-gr-antd-context-key";
function J(n) {
  var c;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = R(), i = W({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  e && e.subscribe((u) => {
    i.slotKey.set(u);
  }), Q();
  const s = V(H), t = ((c = g(s)) == null ? void 0 : c.as_item) || n.as_item, l = s ? t ? g(s)[t] : g(s) : {}, o = h({
    ...n,
    ...l
  });
  return s ? (s.subscribe((u) => {
    const {
      as_item: a
    } = g(o);
    a && (u = u[a]), o.update((d) => ({
      ...d,
      ...u
    }));
  }), [o, (u) => {
    const a = u.as_item ? g(s)[u.as_item] : g(s);
    return o.set({
      ...u,
      ...a
    });
  }]) : [o, (u) => {
    o.set(u);
  }];
}
const z = "$$ms-gr-antd-slot-key";
function Q() {
  N(z, h(void 0));
}
function R() {
  return V(z);
}
const T = "$$ms-gr-antd-component-slot-context-key";
function W({
  slot: n,
  index: e,
  subIndex: i
}) {
  return N(T, {
    slotKey: h(n),
    slotIndex: h(e),
    subSlotIndex: h(i)
  });
}
function $(n) {
  return n && n.__esModule && Object.prototype.hasOwnProperty.call(n, "default") ? n.default : n;
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
    function i() {
      for (var l = "", o = 0; o < arguments.length; o++) {
        var c = arguments[o];
        c && (l = t(l, s(c)));
      }
      return l;
    }
    function s(l) {
      if (typeof l == "string" || typeof l == "number")
        return l;
      if (typeof l != "object")
        return "";
      if (Array.isArray(l))
        return i.apply(null, l);
      if (l.toString !== Object.prototype.toString && !l.toString.toString().includes("[native code]"))
        return l.toString();
      var o = "";
      for (var c in l)
        e.call(l, c) && l[c] && (o = t(o, c));
      return o;
    }
    function t(l, o) {
      return o ? l ? l + " " + o : l + o : l;
    }
    n.exports ? (i.default = i, n.exports = i) : window.classNames = i;
  })();
})(U);
var ee = U.exports;
const te = /* @__PURE__ */ $(ee), {
  getContext: ne,
  setContext: se
} = window.__gradio__svelte__internal;
function ie(n) {
  const e = `$$ms-gr-antd-${n}-context-key`;
  function i(t = ["default"]) {
    const l = t.reduce((o, c) => (o[c] = h([]), o), {});
    return se(e, {
      itemsMap: l,
      allowedSlots: t
    }), l;
  }
  function s() {
    const {
      itemsMap: t,
      allowedSlots: l
    } = ne(e);
    return function(o, c, u) {
      t && (o ? t[o].update((a) => {
        const d = [...a];
        return l.includes(o) ? d[c] = u : d[c] = void 0, d;
      }) : l.includes("default") && t.default.update((a) => {
        const d = [...a];
        return d[c] = u, d;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: s
  };
}
const {
  getItems: Ce,
  getSetItemFn: le
} = ie("radio-group"), {
  SvelteComponent: re,
  check_outros: oe,
  component_subscribe: k,
  create_slot: ue,
  detach: ce,
  empty: ae,
  flush: _,
  get_all_dirty_from_scope: fe,
  get_slot_changes: de,
  group_outros: _e,
  init: me,
  insert: be,
  safe_not_equal: he,
  transition_in: P,
  transition_out: E,
  update_slot_base: ye
} = window.__gradio__svelte__internal;
function M(n) {
  let e;
  const i = (
    /*#slots*/
    n[22].default
  ), s = ue(
    i,
    n,
    /*$$scope*/
    n[21],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(t, l) {
      s && s.m(t, l), e = !0;
    },
    p(t, l) {
      s && s.p && (!e || l & /*$$scope*/
      2097152) && ye(
        s,
        i,
        t,
        /*$$scope*/
        t[21],
        e ? de(
          i,
          /*$$scope*/
          t[21],
          l,
          null
        ) : fe(
          /*$$scope*/
          t[21]
        ),
        null
      );
    },
    i(t) {
      e || (P(s, t), e = !0);
    },
    o(t) {
      E(s, t), e = !1;
    },
    d(t) {
      s && s.d(t);
    }
  };
}
function ge(n) {
  let e, i, s = (
    /*$mergedProps*/
    n[0].visible && M(n)
  );
  return {
    c() {
      s && s.c(), e = ae();
    },
    m(t, l) {
      s && s.m(t, l), be(t, e, l), i = !0;
    },
    p(t, [l]) {
      /*$mergedProps*/
      t[0].visible ? s ? (s.p(t, l), l & /*$mergedProps*/
      1 && P(s, 1)) : (s = M(t), s.c(), P(s, 1), s.m(e.parentNode, e)) : s && (_e(), E(s, 1, 1, () => {
        s = null;
      }), oe());
    },
    i(t) {
      i || (P(s), i = !0);
    },
    o(t) {
      E(s), i = !1;
    },
    d(t) {
      t && ce(e), s && s.d(t);
    }
  };
}
function xe(n, e, i) {
  let s, t, l, o, {
    $$slots: c = {},
    $$scope: u
  } = e, {
    gradio: a
  } = e, {
    props: d = {}
  } = e;
  const m = h(d);
  k(n, m, (r) => i(20, o = r));
  let {
    _internal: b = {}
  } = e, {
    value: f
  } = e, {
    label: y
  } = e, {
    disabled: C
  } = e, {
    title: K
  } = e, {
    required: S
  } = e, {
    as_item: p
  } = e, {
    visible: w = !0
  } = e, {
    elem_id: q = ""
  } = e, {
    elem_classes: v = []
  } = e, {
    elem_style: I = {}
  } = e;
  const O = R();
  k(n, O, (r) => i(19, l = r));
  const [A, X] = J({
    gradio: a,
    props: o,
    _internal: b,
    visible: w,
    elem_id: q,
    elem_classes: v,
    elem_style: I,
    as_item: p,
    value: f,
    label: y,
    disabled: C,
    title: K,
    required: S
  });
  k(n, A, (r) => i(0, t = r));
  const F = G();
  k(n, F, (r) => i(18, s = r));
  const Y = le();
  return n.$$set = (r) => {
    "gradio" in r && i(5, a = r.gradio), "props" in r && i(6, d = r.props), "_internal" in r && i(7, b = r._internal), "value" in r && i(8, f = r.value), "label" in r && i(9, y = r.label), "disabled" in r && i(10, C = r.disabled), "title" in r && i(11, K = r.title), "required" in r && i(12, S = r.required), "as_item" in r && i(13, p = r.as_item), "visible" in r && i(14, w = r.visible), "elem_id" in r && i(15, q = r.elem_id), "elem_classes" in r && i(16, v = r.elem_classes), "elem_style" in r && i(17, I = r.elem_style), "$$scope" in r && i(21, u = r.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*props*/
    64 && m.update((r) => ({
      ...r,
      ...d
    })), n.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value, label, disabled, title, required*/
    1310624 && X({
      gradio: a,
      props: o,
      _internal: b,
      visible: w,
      elem_id: q,
      elem_classes: v,
      elem_style: I,
      as_item: p,
      value: f,
      label: y,
      disabled: C,
      title: K,
      required: S
    }), n.$$.dirty & /*$slotKey, $mergedProps, $slots*/
    786433 && Y(l, t._internal.index || 0, {
      props: {
        style: t.elem_style,
        className: te(t.elem_classes, "ms-gr-antd-radio-group-option"),
        id: t.elem_id,
        value: t.value,
        label: t.label,
        disabled: t.disabled,
        title: t.title,
        required: t.required,
        ...t.props,
        ...D(t)
      },
      slots: s
    });
  }, [t, m, O, A, F, a, d, b, f, y, C, K, S, p, w, q, v, I, s, l, o, u, c];
}
class Ke extends re {
  constructor(e) {
    super(), me(this, e, xe, ge, he, {
      gradio: 5,
      props: 6,
      _internal: 7,
      value: 8,
      label: 9,
      disabled: 10,
      title: 11,
      required: 12,
      as_item: 13,
      visible: 14,
      elem_id: 15,
      elem_classes: 16,
      elem_style: 17
    });
  }
  get gradio() {
    return this.$$.ctx[5];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), _();
  }
  get props() {
    return this.$$.ctx[6];
  }
  set props(e) {
    this.$$set({
      props: e
    }), _();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), _();
  }
  get value() {
    return this.$$.ctx[8];
  }
  set value(e) {
    this.$$set({
      value: e
    }), _();
  }
  get label() {
    return this.$$.ctx[9];
  }
  set label(e) {
    this.$$set({
      label: e
    }), _();
  }
  get disabled() {
    return this.$$.ctx[10];
  }
  set disabled(e) {
    this.$$set({
      disabled: e
    }), _();
  }
  get title() {
    return this.$$.ctx[11];
  }
  set title(e) {
    this.$$set({
      title: e
    }), _();
  }
  get required() {
    return this.$$.ctx[12];
  }
  set required(e) {
    this.$$set({
      required: e
    }), _();
  }
  get as_item() {
    return this.$$.ctx[13];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), _();
  }
  get visible() {
    return this.$$.ctx[14];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), _();
  }
  get elem_id() {
    return this.$$.ctx[15];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), _();
  }
  get elem_classes() {
    return this.$$.ctx[16];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), _();
  }
  get elem_style() {
    return this.$$.ctx[17];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), _();
  }
}
export {
  Ke as default
};
