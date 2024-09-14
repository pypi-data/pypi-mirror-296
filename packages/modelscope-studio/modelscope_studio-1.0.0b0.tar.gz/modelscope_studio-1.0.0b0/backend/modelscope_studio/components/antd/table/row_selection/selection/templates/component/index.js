function U(e) {
  const {
    gradio: t,
    _internal: i,
    ...n
  } = e;
  return Object.keys(i).reduce((s, o) => {
    const l = o.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], c = u.split("_"), _ = (...m) => {
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
        s[c[0]] = m;
        for (let f = 1; f < c.length - 1; f++) {
          const h = {
            ...n.props[c[f]] || {}
          };
          m[c[f]] = h, m = h;
        }
        const b = c[c.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = _, s;
      }
      const a = c[0];
      s[`on${a.slice(0, 1).toUpperCase()}${a.slice(1)}`] = _;
    }
    return s;
  }, {});
}
function k() {
}
function X(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function Y(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return k;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(e) {
  let t;
  return Y(e, (i) => t = i)(), t;
}
const x = [];
function y(e, t = k) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function s(u) {
    if (X(e, u) && (e = u, i)) {
      const c = !x.length;
      for (const _ of n)
        _[1](), x.push(_, e);
      if (c) {
        for (let _ = 0; _ < x.length; _ += 2)
          x[_][0](x[_ + 1]);
        x.length = 0;
      }
    }
  }
  function o(u) {
    s(u(e));
  }
  function l(u, c = k) {
    const _ = [u, c];
    return n.add(_), n.size === 1 && (i = t(s, o) || k), u(e), () => {
      n.delete(_), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: s,
    update: o,
    subscribe: l
  };
}
const {
  getContext: F,
  setContext: P
} = window.__gradio__svelte__internal, D = "$$ms-gr-antd-slots-key";
function L() {
  const e = y({});
  return P(D, e);
}
const Z = "$$ms-gr-antd-context-key";
function B(e) {
  var u;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = M(), i = J({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((c) => {
    i.slotKey.set(c);
  }), G();
  const n = F(Z), s = ((u = g(n)) == null ? void 0 : u.as_item) || e.as_item, o = n ? s ? g(n)[s] : g(n) : {}, l = y({
    ...e,
    ...o
  });
  return n ? (n.subscribe((c) => {
    const {
      as_item: _
    } = g(l);
    _ && (c = c[_]), l.update((a) => ({
      ...a,
      ...c
    }));
  }), [l, (c) => {
    const _ = c.as_item ? g(n)[c.as_item] : g(n);
    return l.set({
      ...c,
      ..._
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const A = "$$ms-gr-antd-slot-key";
function G() {
  P(A, y(void 0));
}
function M() {
  return F(A);
}
const H = "$$ms-gr-antd-component-slot-context-key";
function J({
  slot: e,
  index: t,
  subIndex: i
}) {
  return P(H, {
    slotKey: y(e),
    slotIndex: y(t),
    subSlotIndex: y(i)
  });
}
function Q(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var V = {
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
    function i() {
      for (var o = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (o = s(o, n(u)));
      }
      return o;
    }
    function n(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return i.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var l = "";
      for (var u in o)
        t.call(o, u) && o[u] && (l = s(l, u));
      return l;
    }
    function s(o, l) {
      return l ? o ? o + " " + l : o + l : o;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(V);
var T = V.exports;
const W = /* @__PURE__ */ Q(T), {
  getContext: $,
  setContext: tt
} = window.__gradio__svelte__internal;
function et(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function i(s = ["default"]) {
    const o = s.reduce((l, u) => (l[u] = y([]), l), {});
    return tt(t, {
      itemsMap: o,
      allowedSlots: s
    }), o;
  }
  function n() {
    const {
      itemsMap: s,
      allowedSlots: o
    } = $(t);
    return function(l, u, c) {
      s && (l ? s[l].update((_) => {
        const a = [..._];
        return o.includes(l) ? a[u] = c : a[u] = void 0, a;
      }) : o.includes("default") && s.default.update((_) => {
        const a = [..._];
        return a[u] = c, a;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: n
  };
}
const {
  getItems: ht,
  getSetItemFn: nt
} = et("table-row-selection-selection"), {
  SvelteComponent: st,
  check_outros: it,
  component_subscribe: I,
  create_slot: ot,
  detach: lt,
  empty: rt,
  flush: d,
  get_all_dirty_from_scope: ct,
  get_slot_changes: ut,
  group_outros: _t,
  init: ft,
  insert: at,
  safe_not_equal: mt,
  transition_in: v,
  transition_out: j,
  update_slot_base: dt
} = window.__gradio__svelte__internal;
function q(e) {
  let t;
  const i = (
    /*#slots*/
    e[19].default
  ), n = ot(
    i,
    e,
    /*$$scope*/
    e[18],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(s, o) {
      n && n.m(s, o), t = !0;
    },
    p(s, o) {
      n && n.p && (!t || o & /*$$scope*/
      262144) && dt(
        n,
        i,
        s,
        /*$$scope*/
        s[18],
        t ? ut(
          i,
          /*$$scope*/
          s[18],
          o,
          null
        ) : ct(
          /*$$scope*/
          s[18]
        ),
        null
      );
    },
    i(s) {
      t || (v(n, s), t = !0);
    },
    o(s) {
      j(n, s), t = !1;
    },
    d(s) {
      n && n.d(s);
    }
  };
}
function bt(e) {
  let t, i, n = (
    /*$mergedProps*/
    e[0].visible && q(e)
  );
  return {
    c() {
      n && n.c(), t = rt();
    },
    m(s, o) {
      n && n.m(s, o), at(s, t, o), i = !0;
    },
    p(s, [o]) {
      /*$mergedProps*/
      s[0].visible ? n ? (n.p(s, o), o & /*$mergedProps*/
      1 && v(n, 1)) : (n = q(s), n.c(), v(n, 1), n.m(t.parentNode, t)) : n && (_t(), j(n, 1, 1, () => {
        n = null;
      }), it());
    },
    i(s) {
      i || (v(n), i = !0);
    },
    o(s) {
      j(n), i = !1;
    },
    d(s) {
      s && lt(t), n && n.d(s);
    }
  };
}
function yt(e, t, i) {
  let n, s, o, l, {
    $$slots: u = {},
    $$scope: c
  } = t, {
    gradio: _
  } = t, {
    props: a = {}
  } = t;
  const m = y(a);
  I(e, m, (r) => i(17, l = r));
  let {
    _internal: b = {}
  } = t, {
    as_item: f
  } = t, {
    text: h
  } = t, {
    built_in_selection: p
  } = t, {
    visible: S = !0
  } = t, {
    elem_id: C = ""
  } = t, {
    elem_classes: K = []
  } = t, {
    elem_style: w = {}
  } = t;
  const E = M();
  I(e, E, (r) => i(16, o = r));
  const [N, z] = B({
    gradio: _,
    props: l,
    _internal: b,
    visible: S,
    elem_id: C,
    elem_classes: K,
    elem_style: w,
    as_item: f,
    text: h,
    built_in_selection: p
  });
  I(e, N, (r) => i(0, s = r));
  const O = L();
  I(e, O, (r) => i(15, n = r));
  const R = nt();
  return e.$$set = (r) => {
    "gradio" in r && i(5, _ = r.gradio), "props" in r && i(6, a = r.props), "_internal" in r && i(7, b = r._internal), "as_item" in r && i(8, f = r.as_item), "text" in r && i(9, h = r.text), "built_in_selection" in r && i(10, p = r.built_in_selection), "visible" in r && i(11, S = r.visible), "elem_id" in r && i(12, C = r.elem_id), "elem_classes" in r && i(13, K = r.elem_classes), "elem_style" in r && i(14, w = r.elem_style), "$$scope" in r && i(18, c = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    64 && m.update((r) => ({
      ...r,
      ...a
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, text, built_in_selection*/
    163744 && z({
      gradio: _,
      props: l,
      _internal: b,
      visible: S,
      elem_id: C,
      elem_classes: K,
      elem_style: w,
      as_item: f,
      text: h,
      built_in_selection: p
    }), e.$$.dirty & /*$slotKey, $mergedProps, $slots*/
    98305 && R(o, s._internal.index || 0, s.built_in_selection ? s.built_in_selection : {
      props: {
        style: s.elem_style,
        className: W(s.elem_classes, "ms-gr-antd-table-selection"),
        id: s.elem_id,
        text: s.text,
        ...s.props,
        ...U(s)
      },
      slots: n
    });
  }, [s, m, E, N, O, _, a, b, f, h, p, S, C, K, w, n, o, l, c, u];
}
class gt extends st {
  constructor(t) {
    super(), ft(this, t, yt, bt, mt, {
      gradio: 5,
      props: 6,
      _internal: 7,
      as_item: 8,
      text: 9,
      built_in_selection: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[5];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), d();
  }
  get props() {
    return this.$$.ctx[6];
  }
  set props(t) {
    this.$$set({
      props: t
    }), d();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), d();
  }
  get as_item() {
    return this.$$.ctx[8];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), d();
  }
  get text() {
    return this.$$.ctx[9];
  }
  set text(t) {
    this.$$set({
      text: t
    }), d();
  }
  get built_in_selection() {
    return this.$$.ctx[10];
  }
  set built_in_selection(t) {
    this.$$set({
      built_in_selection: t
    }), d();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), d();
  }
}
export {
  gt as default
};
