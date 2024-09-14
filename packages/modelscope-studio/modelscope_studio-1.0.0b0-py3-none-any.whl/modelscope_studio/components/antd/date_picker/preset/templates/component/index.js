function U(t) {
  const {
    gradio: e,
    _internal: i,
    ...n
  } = t;
  return Object.keys(i).reduce((s, l) => {
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
        return e.dispatch(u.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: b,
          component: n
        });
      };
      if (c.length > 1) {
        let m = {
          ...n.props[c[0]] || {}
        };
        s[c[0]] = m;
        for (let f = 1; f < c.length - 1; f++) {
          const h = {
            ...n.props[c[f]] || {}
          };
          m[c[f]] = h, m = h;
        }
        const b = c[c.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = a, s;
      }
      const _ = c[0];
      s[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = a;
    }
    return s;
  }, {});
}
function I() {
}
function X(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function Y(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return I;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(t) {
  let e;
  return Y(t, (i) => e = i)(), e;
}
const p = [];
function y(t, e = I) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function s(u) {
    if (X(t, u) && (t = u, i)) {
      const c = !p.length;
      for (const a of n)
        a[1](), p.push(a, t);
      if (c) {
        for (let a = 0; a < p.length; a += 2)
          p[a][0](p[a + 1]);
        p.length = 0;
      }
    }
  }
  function l(u) {
    s(u(t));
  }
  function o(u, c = I) {
    const a = [u, c];
    return n.add(a), n.size === 1 && (i = e(s, l) || I), u(t), () => {
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
  getContext: A,
  setContext: P
} = window.__gradio__svelte__internal, D = "$$ms-gr-antd-slots-key";
function L() {
  const t = y({});
  return P(D, t);
}
const Z = "$$ms-gr-antd-context-key";
function B(t) {
  var u;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = M(), i = J({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    i.slotKey.set(c);
  }), G();
  const n = A(Z), s = ((u = g(n)) == null ? void 0 : u.as_item) || t.as_item, l = n ? s ? g(n)[s] : g(n) : {}, o = y({
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
const F = "$$ms-gr-antd-slot-key";
function G() {
  P(F, y(void 0));
}
function M() {
  return A(F);
}
const H = "$$ms-gr-antd-component-slot-context-key";
function J({
  slot: t,
  index: e,
  subIndex: i
}) {
  return P(H, {
    slotKey: y(t),
    slotIndex: y(e),
    subSlotIndex: y(i)
  });
}
function Q(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var V = {
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
})(V);
var T = V.exports;
const W = /* @__PURE__ */ Q(T), {
  getContext: $,
  setContext: ee
} = window.__gradio__svelte__internal;
function te(t) {
  const e = `$$ms-gr-antd-${t}-context-key`;
  function i(s = ["default"]) {
    const l = s.reduce((o, u) => (o[u] = y([]), o), {});
    return ee(e, {
      itemsMap: l,
      allowedSlots: s
    }), l;
  }
  function n() {
    const {
      itemsMap: s,
      allowedSlots: l
    } = $(e);
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
  getItems: he,
  getSetItemFn: ne
} = te("date-picker"), {
  SvelteComponent: se,
  check_outros: ie,
  component_subscribe: w,
  create_slot: le,
  detach: oe,
  empty: re,
  flush: d,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ue,
  group_outros: ae,
  init: fe,
  insert: _e,
  safe_not_equal: me,
  transition_in: k,
  transition_out: j,
  update_slot_base: de
} = window.__gradio__svelte__internal;
function q(t) {
  let e;
  const i = (
    /*#slots*/
    t[19].default
  ), n = le(
    i,
    t,
    /*$$scope*/
    t[18],
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
      262144) && de(
        n,
        i,
        s,
        /*$$scope*/
        s[18],
        e ? ue(
          i,
          /*$$scope*/
          s[18],
          l,
          null
        ) : ce(
          /*$$scope*/
          s[18]
        ),
        null
      );
    },
    i(s) {
      e || (k(n, s), e = !0);
    },
    o(s) {
      j(n, s), e = !1;
    },
    d(s) {
      n && n.d(s);
    }
  };
}
function be(t) {
  let e, i, n = (
    /*$mergedProps*/
    t[0].visible && q(t)
  );
  return {
    c() {
      n && n.c(), e = re();
    },
    m(s, l) {
      n && n.m(s, l), _e(s, e, l), i = !0;
    },
    p(s, [l]) {
      /*$mergedProps*/
      s[0].visible ? n ? (n.p(s, l), l & /*$mergedProps*/
      1 && k(n, 1)) : (n = q(s), n.c(), k(n, 1), n.m(e.parentNode, e)) : n && (ae(), j(n, 1, 1, () => {
        n = null;
      }), ie());
    },
    i(s) {
      i || (k(n), i = !0);
    },
    o(s) {
      j(n), i = !1;
    },
    d(s) {
      s && oe(e), n && n.d(s);
    }
  };
}
function ye(t, e, i) {
  let n, s, l, o, {
    $$slots: u = {},
    $$scope: c
  } = e, {
    gradio: a
  } = e, {
    props: _ = {}
  } = e;
  const m = y(_);
  w(t, m, (r) => i(17, o = r));
  let {
    _internal: b = {}
  } = e, {
    label: f
  } = e, {
    value: h
  } = e, {
    as_item: x
  } = e, {
    visible: C = !0
  } = e, {
    elem_id: K = ""
  } = e, {
    elem_classes: S = []
  } = e, {
    elem_style: v = {}
  } = e;
  const E = M();
  w(t, E, (r) => i(16, l = r));
  const [N, z] = B({
    gradio: a,
    props: o,
    _internal: b,
    visible: C,
    elem_id: K,
    elem_classes: S,
    elem_style: v,
    as_item: x,
    value: h,
    label: f
  });
  w(t, N, (r) => i(0, s = r));
  const O = L();
  w(t, O, (r) => i(15, n = r));
  const R = ne();
  return t.$$set = (r) => {
    "gradio" in r && i(5, a = r.gradio), "props" in r && i(6, _ = r.props), "_internal" in r && i(7, b = r._internal), "label" in r && i(8, f = r.label), "value" in r && i(9, h = r.value), "as_item" in r && i(10, x = r.as_item), "visible" in r && i(11, C = r.visible), "elem_id" in r && i(12, K = r.elem_id), "elem_classes" in r && i(13, S = r.elem_classes), "elem_style" in r && i(14, v = r.elem_style), "$$scope" in r && i(18, c = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    64 && m.update((r) => ({
      ...r,
      ..._
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value, label*/
    163744 && z({
      gradio: a,
      props: o,
      _internal: b,
      visible: C,
      elem_id: K,
      elem_classes: S,
      elem_style: v,
      as_item: x,
      value: h,
      label: f
    }), t.$$.dirty & /*$slotKey, $mergedProps, $slots*/
    98305 && R(l, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: W(s.elem_classes, "ms-gr-antd-date-picker-preset"),
        id: s.elem_id,
        label: s.label,
        value: s.value,
        ...s.props,
        ...U(s)
      },
      slots: n
    });
  }, [s, m, E, N, O, a, _, b, f, h, x, C, K, S, v, n, l, o, c, u];
}
class ge extends se {
  constructor(e) {
    super(), fe(this, e, ye, be, me, {
      gradio: 5,
      props: 6,
      _internal: 7,
      label: 8,
      value: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[5];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), d();
  }
  get props() {
    return this.$$.ctx[6];
  }
  set props(e) {
    this.$$set({
      props: e
    }), d();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), d();
  }
  get label() {
    return this.$$.ctx[8];
  }
  set label(e) {
    this.$$set({
      label: e
    }), d();
  }
  get value() {
    return this.$$.ctx[9];
  }
  set value(e) {
    this.$$set({
      value: e
    }), d();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), d();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), d();
  }
}
export {
  ge as default
};
