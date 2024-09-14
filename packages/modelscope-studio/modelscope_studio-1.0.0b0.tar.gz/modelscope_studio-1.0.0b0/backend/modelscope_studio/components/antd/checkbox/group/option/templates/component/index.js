function X(t) {
  const {
    gradio: e,
    _internal: i,
    ...n
  } = t;
  return Object.keys(i).reduce((s, l) => {
    const o = l.match(/bind_(.+)_event/);
    if (o) {
      const u = o[1], c = u.split("_"), a = (...d) => {
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
        return e.dispatch(u.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: b,
          component: n
        });
      };
      if (c.length > 1) {
        let d = {
          ...n.props[c[0]] || {}
        };
        s[c[0]] = d;
        for (let f = 1; f < c.length - 1; f++) {
          const h = {
            ...n.props[c[f]] || {}
          };
          d[c[f]] = h, d = h;
        }
        const b = c[c.length - 1];
        return d[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = a, s;
      }
      const _ = c[0];
      s[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = a;
    }
    return s;
  }, {});
}
function k() {
}
function Y(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function D(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return k;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(t) {
  let e;
  return D(t, (i) => e = i)(), e;
}
const x = [];
function y(t, e = k) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function s(u) {
    if (Y(t, u) && (t = u, i)) {
      const c = !x.length;
      for (const a of n)
        a[1](), x.push(a, t);
      if (c) {
        for (let a = 0; a < x.length; a += 2)
          x[a][0](x[a + 1]);
        x.length = 0;
      }
    }
  }
  function l(u) {
    s(u(t));
  }
  function o(u, c = k) {
    const a = [u, c];
    return n.add(a), n.size === 1 && (i = e(s, l) || k), u(t), () => {
      n.delete(a), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: s,
    update: l,
    subscribe: o
  };
}
const {
  getContext: F,
  setContext: E
} = window.__gradio__svelte__internal, L = "$$ms-gr-antd-slots-key";
function Z() {
  const t = y({});
  return E(L, t);
}
const B = "$$ms-gr-antd-context-key";
function G(t) {
  var u;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = V(), i = Q({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    i.slotKey.set(c);
  }), H();
  const n = F(B), s = ((u = g(n)) == null ? void 0 : u.as_item) || t.as_item, l = n ? s ? g(n)[s] : g(n) : {}, o = y({
    ...t,
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
const M = "$$ms-gr-antd-slot-key";
function H() {
  E(M, y(void 0));
}
function V() {
  return F(M);
}
const J = "$$ms-gr-antd-component-slot-context-key";
function Q({
  slot: t,
  index: e,
  subIndex: i
}) {
  return E(J, {
    slotKey: y(t),
    slotIndex: y(e),
    subSlotIndex: y(i)
  });
}
function T(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var z = {
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
    function i() {
      for (var l = "", o = 0; o < arguments.length; o++) {
        var u = arguments[o];
        u && (l = s(l, n(u)));
      }
      return l;
    }
    function n(l) {
      if (typeof l == "string" || typeof l == "number")
        return l;
      if (typeof l != "object")
        return "";
      if (Array.isArray(l))
        return i.apply(null, l);
      if (l.toString !== Object.prototype.toString && !l.toString.toString().includes("[native code]"))
        return l.toString();
      var o = "";
      for (var u in l)
        e.call(l, u) && l[u] && (o = s(o, u));
      return o;
    }
    function s(l, o) {
      return o ? l ? l + " " + o : l + o : l;
    }
    t.exports ? (i.default = i, t.exports = i) : window.classNames = i;
  })();
})(z);
var W = z.exports;
const $ = /* @__PURE__ */ T(W), {
  getContext: ee,
  setContext: te
} = window.__gradio__svelte__internal;
function ne(t) {
  const e = `$$ms-gr-antd-${t}-context-key`;
  function i(s = ["default"]) {
    const l = s.reduce((o, u) => (o[u] = y([]), o), {});
    return te(e, {
      itemsMap: l,
      allowedSlots: s
    }), l;
  }
  function n() {
    const {
      itemsMap: s,
      allowedSlots: l
    } = ee(e);
    return function(o, u, c) {
      s && (o ? s[o].update((a) => {
        const _ = [...a];
        return l.includes(o) ? _[u] = c : _[u] = void 0, _;
      }) : l.includes("default") && s.default.update((a) => {
        const _ = [...a];
        return _[u] = c, _;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: n
  };
}
const {
  getItems: ge,
  getSetItemFn: se
} = ne("checkbox-group"), {
  SvelteComponent: ie,
  check_outros: le,
  component_subscribe: I,
  create_slot: oe,
  detach: re,
  empty: ce,
  flush: m,
  get_all_dirty_from_scope: ue,
  get_slot_changes: ae,
  group_outros: fe,
  init: _e,
  insert: de,
  safe_not_equal: me,
  transition_in: j,
  transition_out: P,
  update_slot_base: be
} = window.__gradio__svelte__internal;
function A(t) {
  let e;
  const i = (
    /*#slots*/
    t[20].default
  ), n = oe(
    i,
    t,
    /*$$scope*/
    t[19],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(s, l) {
      n && n.m(s, l), e = !0;
    },
    p(s, l) {
      n && n.p && (!e || l & /*$$scope*/
      524288) && be(
        n,
        i,
        s,
        /*$$scope*/
        s[19],
        e ? ae(
          i,
          /*$$scope*/
          s[19],
          l,
          null
        ) : ue(
          /*$$scope*/
          s[19]
        ),
        null
      );
    },
    i(s) {
      e || (j(n, s), e = !0);
    },
    o(s) {
      P(n, s), e = !1;
    },
    d(s) {
      n && n.d(s);
    }
  };
}
function ye(t) {
  let e, i, n = (
    /*$mergedProps*/
    t[0].visible && A(t)
  );
  return {
    c() {
      n && n.c(), e = ce();
    },
    m(s, l) {
      n && n.m(s, l), de(s, e, l), i = !0;
    },
    p(s, [l]) {
      /*$mergedProps*/
      s[0].visible ? n ? (n.p(s, l), l & /*$mergedProps*/
      1 && j(n, 1)) : (n = A(s), n.c(), j(n, 1), n.m(e.parentNode, e)) : n && (fe(), P(n, 1, 1, () => {
        n = null;
      }), le());
    },
    i(s) {
      i || (j(n), i = !0);
    },
    o(s) {
      P(n), i = !1;
    },
    d(s) {
      s && re(e), n && n.d(s);
    }
  };
}
function he(t, e, i) {
  let n, s, l, o, {
    $$slots: u = {},
    $$scope: c
  } = e, {
    gradio: a
  } = e, {
    props: _ = {}
  } = e;
  const d = y(_);
  I(t, d, (r) => i(18, o = r));
  let {
    _internal: b = {}
  } = e, {
    value: f
  } = e, {
    label: h
  } = e, {
    disabled: p
  } = e, {
    as_item: C
  } = e, {
    visible: K = !0
  } = e, {
    elem_id: S = ""
  } = e, {
    elem_classes: v = []
  } = e, {
    elem_style: w = {}
  } = e;
  const N = V();
  I(t, N, (r) => i(17, l = r));
  const [O, R] = G({
    gradio: a,
    props: o,
    _internal: b,
    visible: K,
    elem_id: S,
    elem_classes: v,
    elem_style: w,
    as_item: C,
    value: f,
    label: h,
    disabled: p
  });
  I(t, O, (r) => i(0, s = r));
  const q = Z();
  I(t, q, (r) => i(16, n = r));
  const U = se();
  return t.$$set = (r) => {
    "gradio" in r && i(5, a = r.gradio), "props" in r && i(6, _ = r.props), "_internal" in r && i(7, b = r._internal), "value" in r && i(8, f = r.value), "label" in r && i(9, h = r.label), "disabled" in r && i(10, p = r.disabled), "as_item" in r && i(11, C = r.as_item), "visible" in r && i(12, K = r.visible), "elem_id" in r && i(13, S = r.elem_id), "elem_classes" in r && i(14, v = r.elem_classes), "elem_style" in r && i(15, w = r.elem_style), "$$scope" in r && i(19, c = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    64 && d.update((r) => ({
      ...r,
      ..._
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value, label, disabled*/
    327584 && R({
      gradio: a,
      props: o,
      _internal: b,
      visible: K,
      elem_id: S,
      elem_classes: v,
      elem_style: w,
      as_item: C,
      value: f,
      label: h,
      disabled: p
    }), t.$$.dirty & /*$slotKey, $mergedProps, $slots*/
    196609 && U(l, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: $(s.elem_classes, "ms-gr-antd-checkbox-group-option"),
        id: s.elem_id,
        value: s.value,
        label: s.label,
        disabled: s.disabled,
        ...s.props,
        ...X(s)
      },
      slots: n
    });
  }, [s, d, N, O, q, a, _, b, f, h, p, C, K, S, v, w, n, l, o, c, u];
}
class xe extends ie {
  constructor(e) {
    super(), _e(this, e, he, ye, me, {
      gradio: 5,
      props: 6,
      _internal: 7,
      value: 8,
      label: 9,
      disabled: 10,
      as_item: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15
    });
  }
  get gradio() {
    return this.$$.ctx[5];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), m();
  }
  get props() {
    return this.$$.ctx[6];
  }
  set props(e) {
    this.$$set({
      props: e
    }), m();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), m();
  }
  get value() {
    return this.$$.ctx[8];
  }
  set value(e) {
    this.$$set({
      value: e
    }), m();
  }
  get label() {
    return this.$$.ctx[9];
  }
  set label(e) {
    this.$$set({
      label: e
    }), m();
  }
  get disabled() {
    return this.$$.ctx[10];
  }
  set disabled(e) {
    this.$$set({
      disabled: e
    }), m();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), m();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), m();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), m();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), m();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), m();
  }
}
export {
  xe as default
};
